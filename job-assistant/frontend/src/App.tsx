import { useEffect, useMemo, useState } from 'react'
import { Route, Routes, useNavigate, useParams } from 'react-router-dom'
import './App.css'
import { fetchJobMatches } from './api/jobs'
import DashboardLayout from './components/DashBoardLayout'
import EmptyState from './components/EmptyState'
import FilterBar from './components/FilterBar'
import JobCard from './components/JobCard'
import JobDetailPanel from './components/JobDetailPanel'
import Modal from './components/Modal'
import StatsGrid from './components/StatsGrid'
import WelcomeHeader from './components/WelcomeHeader'
import type {
  DashboardSummary,
  JobMatch,
  SourceFilter,
  Stat,
} from './types'

function MainDashboard({
  dismissedJobIds,
  onDismissJob,
}: {
  dismissedJobIds: number[]
  onDismissJob: (jobId: number) => void
}) {
  const [jobMatches, setJobMatches] = useState<JobMatch[]>([])
  const [selectedJobId, setSelectedJobId] = useState<number | null>(null)
  const [search, setSearch] = useState('')
  const [minScore, setMinScore] = useState(0)
  const [sourceFilter, setSourceFilter] = useState<SourceFilter>('ALL')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const loadMatches = async () => {
      try {
        setLoading(true)
        setError('')
        const response = await fetchJobMatches({
          search,
          minScore,
          limit: 50,
        })

        const filteredResponse =
          sourceFilter === 'ALL'
            ? response
            : response.filter((item) => item.job.source === sourceFilter)

        const nextVisibleMatches = filteredResponse.filter(
          (match) => !dismissedJobIds.includes(match.job.id),
        )

        setJobMatches(filteredResponse)
        if (nextVisibleMatches.length > 0) {
          setSelectedJobId((current) => {
            if (current && nextVisibleMatches.some((match) => match.job.id === current)) {
              return current
            }

            return nextVisibleMatches[0].job.id
          })
        } else {
          setSelectedJobId(null)
        }
      } catch (loadError) {
        const message =
          loadError instanceof Error
            ? loadError.message
            : 'Erro ao carregar vagas.'
        setError(message)
      } finally {
        setLoading(false)
      }
    }

    loadMatches()
  }, [search, minScore, sourceFilter])

  const visibleJobMatches = useMemo(
    () => jobMatches.filter((match) => !dismissedJobIds.includes(match.job.id)),
    [dismissedJobIds, jobMatches],
  )

  const selectedMatch = useMemo(
    () =>
      visibleJobMatches.find((match) => match.job.id === selectedJobId) ?? null,
    [selectedJobId, visibleJobMatches],
  )

  const dashboardSummary: DashboardSummary = useMemo(() => {
    const totalJobs = jobMatches.length
    const highestScore = jobMatches.reduce(
      (max, match) => Math.max(max, match.total_score),
      0,
    )
    const companies = new Set(
      jobMatches
        .map((match) => match.job.company)
        .filter((company): company is string => Boolean(company)),
    ).size
    const readyToApply = jobMatches.filter(
      (match) => match.recommendation === 'CANDIDATAR',
    ).length

    return {
      totalJobs,
      highestScore,
      companies,
      readyToApply,
    }
  }, [jobMatches])

  const stats: Stat[] = [
    { title: 'Total de vagas', value: dashboardSummary.totalJobs },
    { title: 'Maior score', value: dashboardSummary.highestScore },
    { title: 'Empresas', value: dashboardSummary.companies },
    { title: 'Prontos para aplicar', value: dashboardSummary.readyToApply },
  ]

  const handleOpenDetail = (jobId: number) => {
    navigate(`/jobs/${jobId}`)
    setSelectedJobId(jobId)
  }

  const handleDiscardJob = (jobId: number) => {
    onDismissJob(jobId)
    setSelectedJobId((current) => (current === jobId ? null : current))
    navigate('/')
  }

  return (
    <DashboardLayout userName="Anderson">
      <div className="page-shell">
        <WelcomeHeader />

        <div className="toolbar-row source-selector-row">
          <div className="source-filter-group" aria-label="Filtrar por origem">
            <button
              type="button"
              className={`source-filter ${sourceFilter === 'ALL' ? 'active' : ''}`}
              onClick={() => setSourceFilter('ALL')}
            >
              Todas
            </button>
            <button
              type="button"
              className={`source-filter ${sourceFilter === 'REMOTIVE' ? 'active' : ''}`}
              onClick={() => setSourceFilter('REMOTIVE')}
            >
              Remotive
            </button>
          </div>
        </div>

        <div className="toolbar-row">
          <FilterBar
            search={search}
            minScore={minScore}
            onSearchChange={setSearch}
            onMinScoreChange={setMinScore}
          />
        </div>

        <StatsGrid stats={stats} />

        <div className="results-layout">
          <section className="job-list-panel">
            {loading && <div className="loading-state">Carregando vagas...</div>}

            {!loading && error && (
              <div className="error-state">{error}</div>
            )}

            {!loading && !error && jobMatches.length === 0 && (
              <EmptyState message="Tente ajustar os filtros ou mudar a origem da busca." />
            )}

            {!loading && !error && jobMatches.length > 0 && (
              <div className="job-list">
                {visibleJobMatches.map((match) => (
                  <JobCard
                    key={match.job.id}
                    match={match}
                    active={selectedJobId === match.job.id}
                    onSelect={handleOpenDetail}
                  />
                ))}
              </div>
            )}
          </section>

          <JobDetailPanel match={selectedMatch} onDiscard={handleDiscardJob} />
        </div>
      </div>
    </DashboardLayout>
  )
}

function JobDetailRoute({
  onDismissJob,
}: {
  onDismissJob: (jobId: number) => void
}) {
  const { jobId } = useParams()
  const [match, setMatch] = useState<JobMatch | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const id = Number(jobId)

    if (!Number.isFinite(id)) {
      setLoading(false)
      setError('Vaga inválida.')
      return
    }

    const loadJob = async () => {
      try {
        setLoading(true)
        setError('')
        const response = await fetchJobMatches({ limit: 50 })
        const found = response.find((item) => item.job.id === id) ?? null
        setMatch(found)
      } catch (loadError) {
        setError(
          loadError instanceof Error
            ? loadError.message
            : 'Não foi possível carregar a vaga.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadJob()
  }, [jobId])

  return (
    <DashboardLayout userName="Anderson">
      <div className="page-shell route-page-shell">
        <div className="detail-route-container">
          {loading && <div className="loading-state">Carregando detalhes...</div>}
          {!loading && error && <div className="error-state">{error}</div>}

          {!loading && !error && match && (
            <Modal
              title={match.job.title}
              onClose={() => navigate('/')}
              open={true}
            >
              <JobDetailPanel
                match={match}
                onDiscard={() => {
                  onDismissJob(match.job.id)
                  navigate('/')
                }}
              />
            </Modal>
          )}
        </div>
      </div>
    </DashboardLayout>
  )
}

function App() {
  const [dismissedJobIds, setDismissedJobIds] = useState<number[]>([])

  const handleDismissJob = (jobId: number) => {
    setDismissedJobIds((current) =>
      current.includes(jobId) ? current : [...current, jobId],
    )
  }

  return (
    <Routes>
      <Route
        path="/"
        element={
          <MainDashboard
            dismissedJobIds={dismissedJobIds}
            onDismissJob={handleDismissJob}
          />
        }
      />
      <Route
        path="/jobs/:jobId"
        element={<JobDetailRoute onDismissJob={handleDismissJob} />}
      />
    </Routes>
  )
}

export default App