import RecommendationBadge from './RecommendationBadge'
import type { JobMatch } from '../types'

interface JobCardProps {
  match: JobMatch
  active: boolean
  onSelect: (jobId: number) => void
}

function JobCard({ match, active, onSelect }: JobCardProps) {
  const { job, total_score, recommendation } = match

  return (
    <button
      type="button"
      className={`job-card ${active ? 'active' : ''}`}
      onClick={() => onSelect(job.id)}
    >
      <div className="job-card-header">
        <div>
          <p className="job-source">{job.source}</p>
          <h3>{job.title}</h3>
        </div>
        <div className="job-score-block">
          <span className="score-value">{total_score}</span>
          <span className="score-label">score</span>
        </div>
      </div>

      <div className="job-meta-row">
        <span>{job.company || 'Empresa não informada'}</span>
        <span>{job.location || 'Localização flexível'}</span>
      </div>

      <div className="job-card-footer">
        <RecommendationBadge recommendation={recommendation} />
        <span className="job-contract">{job.employment_type || 'Contrato flexível'}</span>
      </div>
    </button>
  )
}

export default JobCard
