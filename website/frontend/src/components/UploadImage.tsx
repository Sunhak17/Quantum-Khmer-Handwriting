import { forwardRef, useImperativeHandle, useRef, useState } from 'react'

export interface UploadImageHandle {
  getDataUrl: () => string
  clear: () => void
}

interface UploadImageProps {
  onImageChange: (hasImage: boolean) => void
}

const UploadImage = forwardRef<UploadImageHandle, UploadImageProps>(function UploadImage(
  { onImageChange },
  ref,
) {
  const [preview, setPreview] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useImperativeHandle(ref, () => ({
    getDataUrl: () => preview ?? '',
    clear: () => {
      setPreview(null)
      if (inputRef.current) inputRef.current.value = ''
      onImageChange(false)
    },
  }))

  const handleFile = (file: File | undefined) => {
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => {
      setPreview(reader.result as string)
      onImageChange(true)
    }
    reader.readAsDataURL(file)
  }

  return (
    <div>
      <label className="flex h-64 w-full max-w-160 cursor-pointer items-center justify-center rounded-xl border-2 border-dashed border-red-200 bg-white">
        {preview ? (
          <img src={preview} alt="uploaded letter" className="h-full w-full object-contain p-4" />
        ) : (
          <span className="text-sm text-slate-400">Click to upload an image of one letter</span>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={(e) => handleFile(e.target.files?.[0])}
        />
      </label>
    </div>
  )
})

export default UploadImage
