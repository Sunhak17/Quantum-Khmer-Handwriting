import type { HistoryEntry } from '../types'

interface DrawHistoryProps {
  entries: HistoryEntry[]
  onClear: () => void
}

function toCsv(entries: HistoryEntry[]) {
  const header = [
    'n_qubits',
    'quantum_prediction',
    'quantum_confidence',
    'classical_prediction',
    'classical_confidence',
  ]
  const rows = entries.map((e) => [
    String(e.nQubits),
    e.prediction,
    e.confidence.toFixed(4),
    e.classical_prediction,
    e.classical_confidence.toFixed(4),
  ])
  return [header, ...rows].map((row) => row.map((cell) => `"${cell}"`).join(',')).join('\n')
}

function downloadCsv(entries: HistoryEntry[]) {
  const csv = toCsv(entries)
  const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'prediction_history.csv'
  a.click()
  URL.revokeObjectURL(url)
}

export default function DrawHistory({ entries, onClear }: DrawHistoryProps) {
  if (entries.length === 0) return null

  return (
    <div className="mt-4">
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-slate-600">
          Already drawn ({entries.length})
        </h2>
        <div className="flex gap-3">
          <button
            onClick={() => downloadCsv(entries)}
            className="text-xs font-medium text-slate-400 hover:text-slate-600"
          >
            Export CSV
          </button>
          <button
            onClick={onClear}
            className="text-xs font-medium text-slate-400 hover:text-slate-600"
          >
            Clear history
          </button>
        </div>
      </div>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {entries.map((entry) => (
          <div
            key={entry.id}
            className="flex flex-col gap-2 rounded-lg border border-slate-200 bg-slate-50 p-3"
          >
            <img
              src={entry.cleaned_image}
              alt="drawing"
              className="h-16 w-full rounded border border-slate-200 bg-black object-contain"
            />

            <div className="flex items-center gap-1.5">
              <span className="text-xs text-slate-400">Quantum:</span>
              <span className="khmer-text text-xl font-bold text-red-600">{entry.prediction}</span>
              <span className="text-xs text-slate-400">
                {entry.nQubits}q · {Math.round(entry.confidence * 100)}%
              </span>
            </div>

            <div className="flex items-center gap-1.5">
              <span className="text-xs text-slate-400">Classical:</span>
              <span className="khmer-text text-xl font-bold text-slate-700">
                {entry.classical_prediction}
              </span>
              <span className="text-xs text-slate-400">
                {Math.round(entry.classical_confidence * 100)}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
