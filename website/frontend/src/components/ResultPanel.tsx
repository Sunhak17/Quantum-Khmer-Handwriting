import type { PredictResult } from '../types'

interface PredictionCardProps {
  title: string
  label: string
  confidence: number
  accent: 'red' | 'slate'
}

function PredictionCard({ title, label, confidence, accent }: PredictionCardProps) {
  const pct = Math.round(confidence * 100)
  const isRed = accent === 'red'
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className={`h-1.5 ${isRed ? 'bg-red-500' : 'bg-slate-700'}`} />
      <div className="p-6">
        <p className={`text-xs font-bold tracking-widest uppercase ${isRed ? 'text-red-500' : 'text-slate-500'}`}>
          {title}
        </p>
        <div className="mt-4 flex items-stretch gap-6">
          <div className="flex-1">
            <p className="text-[11px] font-semibold tracking-widest text-slate-400 uppercase">Prediction</p>
            <p className={`khmer-text mt-1 text-7xl leading-none font-bold ${isRed ? 'text-red-600' : 'text-slate-800'}`}>
              {label}
            </p>
          </div>
          <div className="w-px bg-slate-100" />
          <div className="flex flex-1 flex-col justify-center">
            <p className="text-[11px] font-semibold tracking-widest text-slate-400 uppercase">Confidence</p>
            <p className={`mt-1 text-4xl leading-none font-extrabold ${isRed ? 'text-red-500' : 'text-slate-700'}`}>
              {pct}%
            </p>
            <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-100">
              <div
                className={`h-full rounded-full ${isRed ? 'bg-red-500' : 'bg-slate-600'}`}
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

interface ResultPanelProps {
  result: PredictResult | null
  nQubits: number
}

export default function ResultPanel({ result, nQubits }: ResultPanelProps) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4">
      <h2 className="mb-3 text-sm font-semibold text-slate-600">Result</h2>
      {!result && (
        <div className="flex h-full min-h-56 items-center justify-center text-sm text-slate-400">
          Draw a letter and click Predict to see results here.
        </div>
      )}
      {result && (
        <div className="space-y-4">
          <PredictionCard
            title="Classical CNN · Baseline"
            label={result.classical_prediction}
            confidence={result.classical_confidence}
            accent="slate"
          />
          <PredictionCard
            title={`Quantum Model · ${nQubits} Qubits`}
            label={result.prediction}
            confidence={result.confidence}
            accent="red"
          />
          <p className="text-xs text-slate-400">
            Shows only the top prediction. Confidence = how sure the model is.
          </p>
        </div>
      )}
    </section>
  )
}
