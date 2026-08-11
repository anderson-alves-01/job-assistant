import React from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
}

const StatCard: React.FC<StatCardProps> = ({ title, value }) => {
  return (
    <div style={{
      backgroundColor: '#f1f1f1',
      padding: '24px',
      borderRadius: '8px',
      textAlign: 'center',
      minWidth: '200px',
      border: '1px solid #e0e0e0', // Borda sutil
    }}>
      <h3 style={{
        fontSize: '18px',
        color: '#555',
        margin: '0 0 16px 0',
        fontWeight: 'normal',
      }}>
        {title}
      </h3>
      <p style={{
        fontSize: '48px',
        color: '#333',
        margin: 0,
        fontWeight: 'bold',
      }}>
        {value}
      </p>
    </div>
  );
};

export default StatCard;