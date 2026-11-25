import base64
import io
import json
import sys

import numpy as np
import torch
from pennylane import numpy as pnp
from PIL import Image

import config

sys.path.insert(0, str(config.ROOT / "src"))
from cnn_model import CnnFeatureExtractor  # noqa: E402
from preprocess import prepare_image  # noqa: E402
from quantum_model import apply_head, make_qnode  # noqa: E402

BASELINE_FEATURES = 64


def decode_data_url(data_url):
    if data_url.startswith("data:"):
        data_url = data_url.split(",", 1)[1]
    return base64.b64decode(data_url)


_LABEL_MAP_CACHE = {}
_CNN_CACHE = {}
_QUANTUM_CACHE = {}
_BASELINE_CACHE = {}


def _label_map_path(name):
    return config.CLASSICAL_MODELS_DIR / name / "label_map.json"


def _cnn_path(name):
    return config.CLASSICAL_MODELS_DIR / name / "cnn.pt"


def _quantum_path(n_qubits):
    return config.QUANTUM_MODELS_DIR / f"{n_qubits}q" / "best.npz"


def load_label_map(name):
    path = _label_map_path(name)
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        label_map = json.load(f)
    return {v: k for k, v in label_map.items()}


def get_label_map(n_qubits):
    if n_qubits not in _LABEL_MAP_CACHE:
        _LABEL_MAP_CACHE[n_qubits] = load_label_map(f"{n_qubits}q")
    return _LABEL_MAP_CACHE[n_qubits]


def load_cnn(name, n_features, n_classes):
    path = _cnn_path(name)
    if not path.exists():
        return None
    model = CnnFeatureExtractor(n_features, n_classes)
    model.load_state_dict(torch.load(path, map_location="cpu"))
    model.eval()
    return model


def get_cnn_model(n_qubits):
    if n_qubits not in _CNN_CACHE:
        id_to_label = get_label_map(n_qubits)
        _CNN_CACHE[n_qubits] = None if id_to_label is None else load_cnn(f"{n_qubits}q", n_qubits, len(id_to_label))
    return _CNN_CACHE[n_qubits]


def get_baseline_model():
    if "baseline" not in _BASELINE_CACHE:
        id_to_label = load_label_map("baseline")
        model = None if id_to_label is None else load_cnn("baseline", BASELINE_FEATURES, len(id_to_label))
        _BASELINE_CACHE["baseline"] = None if model is None else (model, id_to_label)
    return _BASELINE_CACHE["baseline"]


def get_quantum_model(n_qubits):
    if n_qubits not in _QUANTUM_CACHE:
        path = _quantum_path(n_qubits)
        if not path.exists():
            _QUANTUM_CACHE[n_qubits] = None
        else:
            data = np.load(path)
            weights = pnp.array(data["weights"])
            reupload = bool(data["reupload"]) if "reupload" in data.files else False
            qnode = make_qnode(n_qubits, n_layers=weights.shape[0], reupload=reupload)
            head = (
                np.array(data["head_weight"]),
                np.array(data["head_bias"]),
                float(data["log_scale"]),
            )
            _QUANTUM_CACHE[n_qubits] = (qnode, weights, head)
    return _QUANTUM_CACHE[n_qubits]


def available_qubit_options():
    options = []
    for n in config.QUBIT_SIZES:
        id_to_label = get_label_map(n)
        ready = (
            id_to_label is not None
            and _cnn_path(f"{n}q").exists()
            and _quantum_path(n).exists()
        )
        options.append({
            "n_qubits": n,
            "ready": ready,
            "n_classes": len(id_to_label) if id_to_label else None,
        })
    return options


def classical_prediction(x_tensor, cnn, id_to_label):
    baseline = get_baseline_model()
    if baseline is not None:
        cnn, id_to_label = baseline
    with torch.no_grad():
        probs = torch.softmax(cnn(x_tensor), dim=1).numpy()[0]
    pred_id = int(np.argmax(probs))
    return id_to_label[pred_id], float(probs[pred_id])


def predict_drawing(image_data_url, n_qubits):
    if n_qubits not in config.QUBIT_SIZES:
        raise ValueError(f"n_qubits must be one of {config.QUBIT_SIZES}")

    id_to_label = get_label_map(n_qubits)
    if id_to_label is None:
        raise ValueError(f"No label map for {n_qubits} qubits. Run notebooks/02_classical/01_train_cnn.ipynb first.")

    cnn = get_cnn_model(n_qubits)
    if cnn is None:
        raise ValueError(
            f"No trained CNN for {n_qubits} qubits. Run notebooks/02_classical/01_train_cnn.ipynb first."
        )
    quantum_result = get_quantum_model(n_qubits)
    if quantum_result is None:
        raise ValueError(
            f"No trained quantum model for {n_qubits} qubits. "
            "Run notebooks/03_quantum/02_train_hybrid.ipynb first."
        )

    raw_bytes = decode_data_url(image_data_url)
    image_array = prepare_image(raw_bytes, img_height=config.IMG_HEIGHT, img_width=config.IMG_WIDTH)

    x_tensor = torch.tensor(image_array, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    with torch.no_grad():
        cnn_features = cnn.features(x_tensor).numpy()[0]

    classical_label, classical_confidence = classical_prediction(x_tensor, cnn, id_to_label)

    qnode, weights, head = quantum_result
    n_classes = len(id_to_label)
    raw_output = np.array(qnode(pnp.array(cnn_features), weights))
    head_weight, head_bias, log_scale = head
    probs = apply_head(raw_output, head_weight, head_bias, log_scale)
    pred_id = int(np.argmax(probs))

    ranked = sorted(range(n_classes), key=lambda i: probs[i], reverse=True)[:config.TOP_K]

    return {
        "cleaned_image": prepared_image_to_data_url(image_array),
        "cnn_features": cnn_features.tolist(),
        "n_classes": n_classes,
        "prediction": id_to_label[pred_id],
        "confidence": float(probs[pred_id]),
        "top_predictions": [
            {"label": id_to_label[i], "probability": float(probs[i])} for i in ranked
        ],
        "classical_prediction": classical_label,
        "classical_confidence": classical_confidence,
    }


def prepared_image_to_data_url(image_array):
    img = Image.fromarray((image_array * 255).astype(np.uint8), mode="L")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
