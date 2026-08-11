import React from 'react';

const WelcomeHeader: React.FC = () => {
  return (
    <div style={{ marginBottom: '32px' }}>
      <h2 style={{ fontSize: '2rem', margin: '0 0 8px 0' }}>Bem vindo !</h2>
      <p style={{ fontSize: '1.2rem', color: '#555', margin: 0 }}>
        Veja as melhores vagas encontradas para o seu perfil.
      </p>
    </div>
  );
};

export default WelcomeHeader;