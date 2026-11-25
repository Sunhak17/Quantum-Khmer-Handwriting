import importlib.util
from pathlib import Path

import cv2
import numpy as np

_spec = importlib.util.spec_from_file_location("_src_config", Path(__file__).resolve().parent / "config.py")
_config = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_config)
IMG_HEIGHT, IMG_WIDTH = _config.IMG_HEIGHT, _config.IMG_WIDTH


def _decode_to_gray(image_bytes):
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Could not decode image bytes")
    return img


def prepare_image(image_bytes, img_height=IMG_HEIGHT, img_width=IMG_WIDTH):
    gray = _decode_to_gray(image_bytes)
    inverted = 255 - gray

    _, mask = cv2.threshold(inverted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(np.vstack(contours))
        cropped = inverted[y:y + h, x:x + w]
    else:
        cropped = inverted

    crop_h, crop_w = cropped.shape[:2]
    scale = min(img_width / crop_w, img_height / crop_h)
    new_w, new_h = max(1, round(crop_w * scale)), max(1, round(crop_h * scale))
    resized = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    canvas = np.zeros((img_height, img_width), dtype=np.uint8)
    x_off = (img_width - new_w) // 2
    y_off = (img_height - new_h) // 2
    canvas[y_off:y_off + new_h, x_off:x_off + new_w] = resized

    return canvas.astype(np.float32) / 255.0
