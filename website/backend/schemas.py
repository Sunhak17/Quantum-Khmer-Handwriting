from typing import Optional

from pydantic import BaseModel


class PredictRequest(BaseModel):
    image: str
    n_qubits: int


class TopPrediction(BaseModel):
    label: str
    probability: float


class PredictResponse(BaseModel):
    cleaned_image: str
    cnn_features: list[float]
    n_classes: int
    prediction: str
    confidence: float
    top_predictions: list[TopPrediction]
    classical_prediction: str
    classical_confidence: float


class QubitOption(BaseModel):
    n_qubits: int
    ready: bool
    n_classes: Optional[int]


class HealthResponse(BaseModel):
    status: str
