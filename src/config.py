from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "1_raw"
CLEANED_DIR = DATA_DIR / "2_cleaned"
SYNTH_DIR = DATA_DIR / "synthetic_alphabet"
READY_DIR = DATA_DIR / "3_ready" / "cnn_alphabet"

CLASSICAL_MODELS_DIR = ROOT / "models" / "classical"
QUANTUM_MODELS_DIR = ROOT / "models" / "quantum"

QUBIT_SIZES = [4, 6, 8]
IMG_HEIGHT = 32
IMG_WIDTH = 32

INCLUDE_VOWELS_AND_DIGITS = False

OBSOLETE_CONSONANT_CODEPOINTS = {0x179D, 0x179E}
CONSONANTS = [chr(cp) for cp in range(0x1780, 0x17A3) if cp not in OBSOLETE_CONSONANT_CODEPOINTS]

OBSOLETE_INDEPENDENT_VOWEL_CODEPOINTS = {0x17A3, 0x17A4}
INDEPENDENT_VOWELS = [chr(cp) for cp in range(0x17A3, 0x17B4) if cp not in OBSOLETE_INDEPENDENT_VOWEL_CODEPOINTS]

DIGITS = [chr(cp) for cp in range(0x17E0, 0x17EA)]

ALL_CHARS = CONSONANTS + (INDEPENDENT_VOWELS + DIGITS if INCLUDE_VOWELS_AND_DIGITS else [])
SUBSET_16 = CONSONANTS[:16]
