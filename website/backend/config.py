import importlib.util
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = Path(__file__).resolve().parent
BACKEND_MODELS_DIR = BACKEND_DIR / "models"

_spec = importlib.util.spec_from_file_location("shared_config", ROOT / "src" / "config.py")
_shared_config = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_shared_config)

IMG_HEIGHT = _shared_config.IMG_HEIGHT
IMG_WIDTH = _shared_config.IMG_WIDTH
QUBIT_SIZES = _shared_config.QUBIT_SIZES
READY_DIR = _shared_config.READY_DIR
CLASSICAL_MODELS_DIR_RESEARCH = _shared_config.CLASSICAL_MODELS_DIR
QUANTUM_MODELS_DIR_RESEARCH = _shared_config.QUANTUM_MODELS_DIR

USE_BACKEND_BUNDLE = BACKEND_MODELS_DIR.exists() and any(BACKEND_MODELS_DIR.iterdir())
CLASSICAL_MODELS_DIR = BACKEND_MODELS_DIR / "classical" if USE_BACKEND_BUNDLE else CLASSICAL_MODELS_DIR_RESEARCH
QUANTUM_MODELS_DIR = BACKEND_MODELS_DIR / "quantum" if USE_BACKEND_BUNDLE else QUANTUM_MODELS_DIR_RESEARCH

N_LAYERS_FALLBACK = 10
TOP_K = 5

CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",")]
