import { useEffect, useRef, useState } from 'react'

import { fetchQubitOptions, predict as predictApi } from '../api/client'
import DrawCanvas from '../components/DrawCanvas'
import type { DrawCanvasHandle } from '../components/DrawCanvas'
import QubitSelector from '../components/QubitSelector'
import ResultPanel from '../components/ResultPanel'
import UploadImage from '../components/UploadImage'
import type { UploadImageHandle } from '../components/UploadImage'
import type { PredictResult, QubitOption } from '../types'

type InputMode = 'draw' | 'upload'

interface HomePageProps {
  onPredicted: (result: PredictResult, nQubits: number) => void
}

export default function HomePage({ onPredicted }: HomePageProps) {
  const canvasHandleRef = useRef<DrawCanvasHandle>(null)
  const uploadHandleRef = useRef<UploadImageHandle>(null)
  const [mode, setMode] = useState<InputMode>('draw')
  const [hasDrawing, setHasDrawing] = useState(false)
  const [hasUpload, setHasUpload] = useState(false)
  const [qubitOptions, setQubitOptions] = useState<QubitOption[]>([])
  const [nQubits, setNQubits] = useState(4)
  const [result, setResult] = useState<PredictResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const hasContent = mode === 'draw' ? hasDrawing : hasUpload

  const switchMode = (next: InputMode) => {
    if (next === mode) return
    setMode(next)
    canvasHandleRef.current?.clear()
    uploadHandleRef.current?.clear()
    setResult(null)
    setError(null)
  }

  useEffect(() => {
    fetchQubitOptions()
      .then(setQubitOptions)
      .catch((e: Error) => setError(e.message))
  }, [])

  const clearCanvas = () => {
    canvasHandleRef.current?.clear()
    uploadHandleRef.current?.clear()
    setResult(null)
    setError(null)
  }

  const runPredict = () => {
    const image =
      mode === 'draw' ? canvasHandleRef.current?.getDataUrl() : uploadHandleRef.current?.getDataUrl()
    if (!image) return
    setLoading(true)
    setError(null)
    predictApi(image, nQubits)
      .then((data) => {
        setResult(data)
        onPredicted(data, nQubits)
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false))
  }

  return (
    <main className="space-y-6 px-8 py-6">
      {error && (
        <div className="rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <section>
          <h2 className="mb-2 text-sm font-semibold text-slate-600">Qubit count</h2>
          <QubitSelector options={qubitOptions} value={nQubits} onChange={setNQubits} />

          <div className="mb-2 flex w-fit rounded-lg border border-slate-200 bg-slate-50 p-0.5 text-xs font-medium">
            <button
              onClick={() => switchMode('draw')}
              className={`rounded-md px-3 py-1 ${
                mode === 'draw' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500'
              }`}
            >
              Draw
            </button>
            <button
              onClick={() => switchMode('upload')}
              className={`rounded-md px-3 py-1 ${
                mode === 'upload' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500'
              }`}
            >
              Upload
            </button>
          </div>
          <h2 className="mb-2 text-sm font-semibold text-slate-600">
            {mode === 'draw' ? 'Draw a Khmer letter' : 'Upload a Khmer letter'}
          </h2>
          {mode === 'draw' ? (
            <DrawCanvas ref={canvasHandleRef} onDrawingChange={setHasDrawing} />
          ) : (
            <UploadImage ref={uploadHandleRef} onImageChange={setHasUpload} />
          )}
          <div className="mt-3 flex gap-2">
            <button
              onClick={clearCanvas}
              className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50"
            >
              Clear
            </button>
            <button
              onClick={runPredict}
              disabled={!hasContent || loading}
              className="rounded-lg bg-red-500 px-4 py-2 text-sm font-medium text-white hover:bg-red-600 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading ? 'Predicting…' : 'Predict'}
            </button>
          </div>
        </section>

        <ResultPanel result={result} nQubits={nQubits} />
      </div>
    </main>
  )
}
