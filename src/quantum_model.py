import numpy as np
import pennylane as qml
from pennylane import numpy as pnp

N_LAYERS = 10
REUPLOAD_MAX_QUBITS = 4


def default_reupload(n_qubits):
    return n_qubits <= REUPLOAD_MAX_QUBITS


def init_weights(n_qubits, n_layers=None, seed=0):
    if n_layers is None:
        n_layers = N_LAYERS
    rng = np.random.default_rng(seed)
    values = rng.uniform(0, 2 * np.pi, size=(n_layers, n_qubits, 2))
    return pnp.array(values, requires_grad=True)


def make_qnode(n_qubits, n_layers=None, noise_prob=0.0, reupload=None):
    if n_layers is None:
        n_layers = N_LAYERS
    if reupload is None:
        reupload = default_reupload(n_qubits)
    dev = qml.device("default.mixed" if noise_prob > 0 else "default.qubit", wires=n_qubits)

    @qml.qnode(dev, interface="autograd")
    def circuit(x, weights):
        def encode():
            for q in range(n_qubits):
                qml.RY(x[..., q], wires=q)
                if noise_prob > 0:
                    qml.DepolarizingChannel(noise_prob, wires=q)

        if not reupload:
            encode()

        for layer_idx in range(n_layers):
            if reupload:
                encode()
            for q in range(n_qubits):
                qml.RY(weights[layer_idx, q, 0], wires=q)
                qml.RZ(weights[layer_idx, q, 1], wires=q)
                if noise_prob > 0:
                    qml.DepolarizingChannel(noise_prob, wires=q)
            for q in range(n_qubits):
                target = (q + 1) % n_qubits
                qml.CNOT(wires=[q, target])
                if noise_prob > 0:
                    qml.DepolarizingChannel(noise_prob, wires=q)
                    qml.DepolarizingChannel(noise_prob, wires=target)

        z = [qml.expval(qml.PauliZ(q)) for q in range(n_qubits)]
        zz = [qml.expval(qml.PauliZ(q) @ qml.PauliZ((q + 1) % n_qubits)) for q in range(n_qubits)]
        return z + zz

    return circuit


def init_head_params(n_qubits, n_classes, seed=0):
    rng = np.random.default_rng(seed + 1)
    feat_dim = 2 * n_qubits
    head_weight = pnp.array(
        rng.normal(0, 1 / np.sqrt(feat_dim), size=(n_classes, feat_dim)), requires_grad=True
    )
    head_bias = pnp.array(np.zeros(n_classes), requires_grad=True)
    log_scale = pnp.array(2.0, requires_grad=True)
    return head_weight, head_bias, log_scale


def apply_head(features, head_weight, head_bias, log_scale):
    logits = pnp.dot(features, head_weight.T) + head_bias
    scaled = logits * pnp.exp(log_scale)
    shifted = scaled - pnp.max(scaled, axis=-1, keepdims=True)
    exp_vals = pnp.exp(shifted)
    return exp_vals / pnp.sum(exp_vals, axis=-1, keepdims=True)


def cross_entropy(probs, labels):
    eps = 1e-10
    idx = np.arange(len(labels))
    return -pnp.mean(pnp.log(probs[idx, labels] + eps))


def accuracy(probs, labels):
    preds = np.argmax(np.array(probs), axis=1)
    return float(np.mean(preds == labels))
