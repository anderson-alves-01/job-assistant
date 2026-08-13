export type Recommendation = 'CANDIDATAR' | 'AVALIAR' | 'DESCARTAR'

export type Job = {
  id: number
  source: string
  external_id: string
  title: string
  company: string | null
  category: string | null
  description: string
  location: string | null
  employment_type: string | null
  salary_text: string | null
  application_url: string
  source_url: string
  published_at: string | null
  content_hash: string
  status: string
  collected_at: string
  updated_at: string
}

export type JobMatch = {
  job: Job
  total_score: number
  recommendation: Recommendation
  title_score: number
  skills_score: number
  location_score: number
  seniority_score: number
  employment_type_score: number
  matched_primary_skills: string[]
  matched_secondary_skills: string[]
  missing_primary_skills: string[]
  rejection_reasons: string[]
  summary: string
}

export type SourceFilter = 'ALL' | 'REMOTIVE'

export type Stat = {
  title: string
  value: string | number
}

export type DashboardSummary = {
  totalJobs: number
  highestScore: number
  companies: number
  readyToApply: number
}
