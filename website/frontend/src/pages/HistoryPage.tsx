import DrawHistory from '../components/DrawHistory'
import type { HistoryEntry } from '../types'

interface HistoryPageProps {
  entries: HistoryEntry[]
  onClear: () => void
}

export default function HistoryPage({ entries, onClear }: HistoryPageProps) {
  return (
    <main className="space-y-6 px-8 py-6">
      {entries.length === 0 ? (
        <div className="flex min-h-56 items-center justify-center text-sm text-slate-400">
          No predictions yet. Go to Predict and draw or upload a letter.
        </div>
      ) : (
        <DrawHistory entries={entries} onClear={onClear} />
      )}
    </main>
  )
}
