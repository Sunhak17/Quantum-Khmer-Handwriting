export interface QubitOption {
  n_qubits: number
  ready: boolean
  n_classes: number | null
}

export interface TopPrediction {
  label: string
  probability: number
}

export interface PredictResult {
  cleaned_image: string
  cnn_features: number[]
  n_classes: number
  prediction: string
  confidence: number
  top_predictions: TopPrediction[]
  classical_prediction: string
  classical_confidence: number
}

export interface HistoryEntry extends PredictResult {
  id: string
  nQubits: number
}
