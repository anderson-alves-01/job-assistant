import { useEffect } from 'react'

interface ModalProps {
  title: string
  open: boolean
  children: React.ReactNode
  onClose: () => void
}

function Modal({ title, open, children, onClose }: ModalProps) {
  useEffect(() => {
    if (!open) {
      return undefined
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [open, onClose])

  if (!open) {
    return null
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(event) => event.stopPropagation()}>
        <div className="modal-header">
          <h3>{title}</h3>
          <button type="button" className="modal-close" onClick={onClose} aria-label="Fechar modal">
            ×
          </button>
        </div>

        <div className="modal-body">{children}</div>
      </div>
    </div>
  )
}

export default Modal
