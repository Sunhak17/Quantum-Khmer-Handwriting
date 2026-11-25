import type { PredictResult, QubitOption } from '../types'

export async function fetchQubitOptions(): Promise<QubitOption[]> {
  try {
    const r = await fetch('/api/qubit-options')
    if (!r.ok) throw new Error()
    return (await r.json()) as QubitOption[]
  } catch {
    throw new Error('Could not reach the backend at /api. Is uvicorn running?')
  }
}

export async function predict(image: string, nQubits: number): Promise<PredictResult> {
  const r = await fetch('/api/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image, n_qubits: nQubits }),
  })
  if (!r.ok) {
    const body = await r.json().catch(() => ({}))
    throw new Error(body.detail || 'prediction failed')
  }
  return r.json() as Promise<PredictResult>
}
