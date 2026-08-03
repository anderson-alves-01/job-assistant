import React from 'react';

const ActionToolbar: React.FC = () => {
  // Dados simulados
  const lastSyncTime = "10:42";

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '24px'
    }}>
      <button style={{
        backgroundColor: '#e0e0e0',
        border: 'none',
        padding: '12px 24px',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '1rem',
      }}>
        Atualizar Vagas
      </button>
      <p style={{ margin: 0, color: '#777' }}>
        Última sync: {lastSyncTime}
      </p>
    </div>
  );
};

export default ActionToolbar;