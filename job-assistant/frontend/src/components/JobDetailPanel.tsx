import RecommendationBadge from './RecommendationBadge'
import type { JobMatch } from '../types'

interface JobDetailPanelProps {
  match: JobMatch | null
  onDiscard?: (jobId: number) => void
}

function JobDetailPanel({ match, onDiscard }: JobDetailPanelProps) {
  if (!match) {
    return (
      <aside className="job-detail-panel empty">
        <p>Selecione uma vaga para ver o resumo detalhado.</p>
      </aside>
    )
  }

  const {
    job,
    total_score,
    recommendation,
    matched_primary_skills,
    matched_secondary_skills,
    missing_primary_skills,
    summary,
    rejection_reasons,
    title_score,
    location_score,
    seniority_score,
    employment_type_score,
    skills_score,
  } = match

  return (
    <aside className="job-detail-panel">
      <div className="job-detail-header">
        <div>
          <p className="job-source">{job.source}</p>
          <h2>{job.title}</h2>
        </div>
        <div className="job-score-block large">
          <span className="score-value">{total_score}</span>
          <span className="score-label">score</span>
        </div>
      </div>

      <div className="detail-summary-row">
        <RecommendationBadge recommendation={recommendation} />
        <span>{job.company || 'Empresa não informada'}</span>
        <span>{job.location || 'Localização flexível'}</span>
        <span>{job.employment_type || 'Contrato flexível'}</span>
      </div>

      <div className="detail-meta-grid">
        <div>
          <span className="meta-label">Cargo</span>
          <strong>{title_score}/20</strong>
        </div>
        <div>
          <span className="meta-label">Skills</span>
          <strong>{skills_score}/40</strong>
        </div>
        <div>
          <span className="meta-label">Localização</span>
          <strong>{location_score}/20</strong>
        </div>
        <div>
          <span className="meta-label">Senioridade</span>
          <strong>{seniority_score}/10</strong>
        </div>
        <div>
          <span className="meta-label">Contrato</span>
          <strong>{employment_type_score}/10</strong>
        </div>
      </div>

      <div className="detail-section">
        <h3>Resumo da aderência</h3>
        <p>{summary}</p>
      </div>

      <div className="detail-section">
        <h3>Skills relevantes</h3>
        <div className="skill-list">
          {matched_primary_skills.length ? matched_primary_skills.map((skill) => (
            <span key={skill} className="skill-pill skill-pill-match">{skill}</span>
          )) : <span className="muted-text">Nenhuma skill principal identificada</span>}
        </div>
      </div>

      <div className="detail-section">
        <h3>Skills complementares</h3>
        <div className="skill-list">
          {matched_secondary_skills.length ? matched_secondary_skills.map((skill) => (
            <span key={skill} className="skill-pill skill-pill-secondary">{skill}</span>
          )) : <span className="muted-text">Sem apontamentos complementares</span>}
        </div>
      </div>

      {missing_primary_skills.length > 0 && (
        <div className="detail-section">
          <h3>Skills pendentes</h3>
          <div className="skill-list">
            {missing_primary_skills.map((skill) => (
              <span key={skill} className="skill-pill skill-pill-missing">{skill}</span>
            ))}
          </div>
        </div>
      )}

      {rejection_reasons.length > 0 && (
        <div className="detail-section warning-box">
          <h3>Motivos de descarte</h3>
          <ul>
            {rejection_reasons.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="detail-actions">
        <a href={job.application_url} target="_blank" rel="noreferrer" className="primary-button">
          Abrir candidatura
        </a>
        <button
          type="button"
          className="secondary-button"
          onClick={() => onDiscard?.(job.id)}
        >
          Descartar Vaga
        </button>
      </div>
    </aside>
  )
}

export default JobDetailPanel
