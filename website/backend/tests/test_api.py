import base64
import io
import sys
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import app  # noqa: E402

client = TestClient(app)


def _sample_drawing_data_url():
    img = Image.new("L", (300, 120), color=255)
    draw = ImageDraw.Draw(img)
    draw.line([(60, 30), (60, 90), (240, 90)], fill=0, width=10)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_qubit_options():
    response = client.get("/api/qubit-options")
    assert response.status_code == 200
    options = response.json()
    assert {o["n_qubits"] for o in options} == {4, 6, 8}
    for option in options:
        assert "ready" in option
        assert "n_classes" in option


def test_predict_contract():
    payload = {"image": _sample_drawing_data_url(), "n_qubits": 4}
    response = client.post("/api/predict", json=payload)

    if response.status_code == 400:
        assert "detail" in response.json()
        return

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["prediction"], str)
    assert 0.0 <= body["confidence"] <= 1.0
    assert isinstance(body["cnn_features"], list)
    assert isinstance(body["top_predictions"], list)
    assert body["top_predictions"]
    for entry in body["top_predictions"]:
        assert "label" in entry and "probability" in entry
    assert isinstance(body["classical_prediction"], str)
    assert 0.0 <= body["classical_confidence"] <= 1.0


def test_predict_rejects_bad_qubit_count():
    payload = {"image": _sample_drawing_data_url(), "n_qubits": 3}
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 400
