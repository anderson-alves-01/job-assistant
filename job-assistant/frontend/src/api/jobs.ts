import type { JobMatch } from '../types'

const API_BASE = '/api'

interface FetchJobMatchesParams {
  search?: string
  minScore?: number
  limit?: number
}

export async function fetchJobMatches({
  search,
  minScore = 0,
  limit = 50,
}: FetchJobMatchesParams = {}): Promise<JobMatch[]> {
  const params = new URLSearchParams()

  if (search && search.trim()) {
    params.set('search', search.trim())
  }

  params.set('min_score', String(minScore))
  params.set('limit', String(limit))

  const response = await fetch(`${API_BASE}/jobs/matches?${params.toString()}`)

  if (!response.ok) {
    const errorBody = await response.text()
    throw new Error(
      errorBody || 'Não foi possível carregar as vagas no momento.'
    )
  }

  return (await response.json()) as JobMatch[]
}

export async function fetchJobById(jobId: number): Promise<JobMatch> {
  const response = await fetch(`${API_BASE}/jobs/${jobId}/match`)

  if (!response.ok) {
    const errorBody = await response.text()
    throw new Error(
      errorBody || 'Não foi possível carregar os detalhes da vaga.'
    )
  }

  return (await response.json()) as JobMatch
}
