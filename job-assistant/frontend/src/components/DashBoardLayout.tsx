import type { ReactNode } from 'react'
import DashboardHeader from './DashBoardHeader'

interface DashboardLayoutProps {
  userName: string
  children: ReactNode
}

function DashboardLayout({ userName, children }: DashboardLayoutProps) {
  return (
    <div className="dashboard-shell">
      <DashboardHeader userName={userName} />
      <main className="dashboard-main">{children}</main>
    </div>
  )
}

export default DashboardLayout