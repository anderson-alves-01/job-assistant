import type { Recommendation } from '../types'

interface RecommendationBadgeProps {
  recommendation: Recommendation
}

const recommendationStyles: Record<Recommendation, { label: string; className: string }> = {
  CANDIDATAR: {
    label: 'Candidatar',
    className: 'badge badge-success',
  },
  AVALIAR: {
    label: 'Avaliar',
    className: 'badge badge-warning',
  },
  DESCARTAR: {
    label: 'Descartar',
    className: 'badge badge-danger',
  },
}

function RecommendationBadge({ recommendation }: RecommendationBadgeProps) {
  const style = recommendationStyles[recommendation]

  return <span className={style.className}>{style.label}</span>
}

export default RecommendationBadge
