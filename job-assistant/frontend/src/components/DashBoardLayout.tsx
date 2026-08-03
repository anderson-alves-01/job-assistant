import React from 'react';
import DashboardHeader from './DashboardHeader';

interface DashboardLayoutProps {
  userName: string;
  children: React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ userName, children }) => {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <DashboardHeader userName={userName} />
      <main style={{ flex: 1, padding: '32px' }}>
        {children}
      </main>
    </div>
  );
};

export default DashboardLayout;