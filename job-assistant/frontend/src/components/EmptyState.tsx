interface EmptyStateProps {
  message: string
}

function EmptyState({ message }: EmptyStateProps) {
  return (
    <div className="empty-state">
      <h3>Nenhuma vaga encontrada</h3>
      <p>{message}</p>
    </div>
  )
}

export default EmptyState
