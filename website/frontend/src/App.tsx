import { useState } from 'react'
import { Route, Routes } from 'react-router-dom'

import NavBar from './components/NavBar'
import HistoryPage from './pages/HistoryPage'
import HomePage from './pages/HomePage'
import type { HistoryEntry, PredictResult } from './types'

export default function App() {
  const [history, setHistory] = useState<HistoryEntry[]>([])

  const addHistoryEntry = (data: PredictResult, nQubits: number) => {
    setHistory((h) => [
      {
        ...data,
        id: crypto.randomUUID(),
        nQubits,
      },
      ...h,
    ])
  }

  return (
    <div className="min-h-screen bg-white">
      <NavBar />
      <Routes>
        <Route path="/" element={<HomePage onPredicted={addHistoryEntry} />} />
        <Route
          path="/history"
          element={
            <HistoryPage entries={history} onClear={() => setHistory([])} />
          }
        />
      </Routes>
    </div>
  )
}
