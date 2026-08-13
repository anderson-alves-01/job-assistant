import StatCard from './StatCard'
import type { Stat } from '../types'

interface StatsGridProps {
  stats: Stat[]
}

function StatsGrid({ stats }: StatsGridProps) {
  return (
    <div className="stats-grid">
      {stats.map((stat) => (
        <StatCard key={stat.title} title={stat.title} value={stat.value} />
      ))}
    </div>
  )
}

export default StatsGrid