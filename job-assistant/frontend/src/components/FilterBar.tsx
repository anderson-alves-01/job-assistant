interface FilterBarProps {
  search: string
  minScore: number
  onSearchChange: (value: string) => void
  onMinScoreChange: (value: number) => void
}

function FilterBar({
  search,
  minScore,
  onSearchChange,
  onMinScoreChange,
}: FilterBarProps) {
  return (
    <div className="filter-bar">
      <label className="search-field">
        <span>Buscar vagas</span>
        <input
          type="search"
          value={search}
          placeholder="Por cargo, empresa ou tecnologia"
          onChange={(event) => onSearchChange(event.target.value)}
        />
      </label>

      <label className="score-field">
        <span>Score mínimo</span>
        <select
          value={minScore}
          onChange={(event) => onMinScoreChange(Number(event.target.value))}
        >
          <option value={0}>Todos</option>
          <option value={60}>60+</option>
          <option value={70}>70+</option>
          <option value={80}>80+</option>
          <option value={90}>90+</option>
        </select>
      </label>
    </div>
  )
}

export default FilterBar
