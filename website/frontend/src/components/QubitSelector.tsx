import type { QubitOption } from '../types'

const QUBIT_SIZES = [4, 6, 8] as const
const SUBSET_16_RANGE = 'ក–ត'

interface QubitSelectorProps {
  options: QubitOption[]
  value: number
  onChange: (n: number) => void
}

function describeClasses(nClasses: number | null | undefined) {
  if (!nClasses) return null
  if (nClasses === 16) {
    return `Knows only the first 16 consonants (${SUBSET_16_RANGE}).`
  }
  return `Knows all ${nClasses} characters.`
}

export default function QubitSelector({ options, value, onChange }: QubitSelectorProps) {
  const note = describeClasses(options.find((o) => o.n_qubits === value)?.n_classes)
  return (
    <div className="mb-4">
      <div className="flex flex-wrap gap-2">
        {QUBIT_SIZES.map((n) => {
          const opt = options.find((o) => o.n_qubits === n)
          return (
            <button
              key={n}
              onClick={() => onChange(n)}
              disabled={opt ? !opt.ready : false}
              className={`rounded-md border px-4 py-1.5 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-40 ${
                value === n
                  ? 'border-red-500 bg-red-500 text-white'
                  : 'border-slate-300 bg-white text-slate-600 hover:border-red-300'
              }`}
            >
              {n} qubits
            </button>
          )
        })}
      </div>
      {note && <p className="khmer-text mt-2 text-xs text-slate-500">{note}</p>}
    </div>
  )
}
