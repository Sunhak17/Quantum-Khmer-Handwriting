import importlib.util
import math
from pathlib import Path

import torch
import torch.nn as nn

_spec = importlib.util.spec_from_file_location("_src_config", Path(__file__).resolve().parent / "config.py")
_config = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_config)
IMG_HEIGHT, IMG_WIDTH = _config.IMG_HEIGHT, _config.IMG_WIDTH

FEATURE_TEMPERATURE = 16.0
_FLAT_SIZE = 16 * (IMG_HEIGHT // 4) * (IMG_WIDTH // 4)


class CnnFeatureExtractor(nn.Module):
    def __init__(self, n_features, n_classes):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.bottleneck = nn.Sequential(
            nn.Flatten(),
            nn.Linear(_FLAT_SIZE, 64), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(64, n_features),
        )
        self.classifier = nn.Linear(n_features, n_classes)

    def encode(self, x):
        z = self.conv(x)
        return self.bottleneck(z)

    def features(self, x):
        return torch.sigmoid(self.encode(x) / FEATURE_TEMPERATURE) * math.pi

    def forward(self, x):
        return self.classifier(self.encode(x))
