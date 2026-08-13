interface DashboardHeaderProps {
  userName: string
}

function DashboardHeader({ userName }: DashboardHeaderProps) {
  return (
    <header className="dashboard-header">
      <div className="brand-block">
        <div className="brand-mark">JA</div>
        <div>
          <p className="brand-label">Job Assistant</p>
        </div>
      </div>

      <div className="profile-pill">{userName}</div>
    </header>
  )
}

export default DashboardHeader