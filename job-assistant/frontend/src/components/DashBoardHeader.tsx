import React from 'react';

interface DashboardHeaderProps {
  userName: string;
}

const DashboardHeader: React.FC<DashboardHeaderProps> = ({ userName }) => {
  return (
    <header style={{
      backgroundColor: '#f1f1f1',
      padding: '16px 32px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      borderBottom: '1px solid #e0e0e0',
    }}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <h1 style={{ margin: '0 8px 0 0', fontWeight: 'bold' }}>JA</h1>
        <p style={{ margin: 0, fontSize: '1.1rem' }}>Job Assistant</p>
      </div>
      <p style={{ margin: 0 }}>{userName}</p>
    </header>
  );
};

export default DashboardHeader;