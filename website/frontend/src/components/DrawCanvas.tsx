import { forwardRef, useEffect, useImperativeHandle, useRef } from 'react'
import type { MouseEvent as ReactMouseEvent, TouchEvent as ReactTouchEvent } from 'react'

const CANVAS_WIDTH = 640
const CANVAS_HEIGHT = 256

export interface DrawCanvasHandle {
  getDataUrl: () => string
  clear: () => void
}

interface DrawCanvasProps {
  onDrawingChange: (hasDrawing: boolean) => void
}

type DrawEvent = ReactMouseEvent<HTMLCanvasElement> | ReactTouchEvent<HTMLCanvasElement>

const DrawCanvas = forwardRef<DrawCanvasHandle, DrawCanvasProps>(function DrawCanvas(
  { onDrawingChange },
  ref,
) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const drawingRef = useRef(false)

  const fillWhite = () => {
    const canvas = canvasRef.current
    const ctx = canvas?.getContext('2d')
    if (!canvas || !ctx) return
    ctx.fillStyle = 'white'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
  }

  useEffect(() => {
    fillWhite()
  }, [])

  useImperativeHandle(ref, () => ({
    getDataUrl: () => canvasRef.current?.toDataURL('image/png') ?? '',
    clear: () => {
      fillWhite()
      onDrawingChange(false)
    },
  }))

  const getPos = (e: DrawEvent) => {
    const canvas = canvasRef.current
    if (!canvas) return { x: 0, y: 0 }
    const rect = canvas.getBoundingClientRect()
    const point = 'touches' in e ? e.touches[0] : e
    return {
      x: ((point.clientX - rect.left) / rect.width) * CANVAS_WIDTH,
      y: ((point.clientY - rect.top) / rect.height) * CANVAS_HEIGHT,
    }
  }

  const startDraw = (e: DrawEvent) => {
    e.preventDefault()
    drawingRef.current = true
    const ctx = canvasRef.current?.getContext('2d')
    if (!ctx) return
    const { x, y } = getPos(e)
    ctx.beginPath()
    ctx.moveTo(x, y)
    onDrawingChange(true)
  }

  const draw = (e: DrawEvent) => {
    if (!drawingRef.current) return
    e.preventDefault()
    const ctx = canvasRef.current?.getContext('2d')
    if (!ctx) return
    const { x, y } = getPos(e)
    ctx.lineTo(x, y)
    ctx.strokeStyle = 'black'
    ctx.lineWidth = 14
    ctx.lineCap = 'round'
    ctx.lineJoin = 'round'
    ctx.stroke()
  }

  const stopDraw = () => {
    drawingRef.current = false
  }

  return (
    <div className="w-full max-w-160">
      <canvas
        ref={canvasRef}
        width={CANVAS_WIDTH}
        height={CANVAS_HEIGHT}
        className="h-64 w-full touch-none rounded-xl border-2 border-dashed border-slate-300 bg-white"
        onMouseDown={startDraw}
        onMouseMove={draw}
        onMouseUp={stopDraw}
        onMouseLeave={stopDraw}
        onTouchStart={startDraw}
        onTouchMove={draw}
        onTouchEnd={stopDraw}
      />
    </div>
  )
})

export default DrawCanvas
