import './App.css' // Importe qualquer estilo global necessário
import DashboardLayout from './components/DashboardLayout'
import WelcomeHeader from './components/WelcomeHeader'
import ActionToolbar from './components/ActionToolbar'
import StatsGrid from './components/StatsGrid'
import { Stat } from './types'

function App() {
  // Dados simulados (Mock) - que viriam do backend futuramente
  const userData = {
    name: 'Anderson'
  };

  const dashboardStats: Stat[] = [
    { title: 'Total de Vagas:', value: 208 },
    { title: 'Maior Score:', value: 98 },
    { title: 'Empresas:', value: 18 },
    { title: 'Perfil:', value: 'Atualizado' },
  ];

  return (
    <DashboardLayout userName={userData.name}>
      <WelcomeHeader />
      <ActionToolbar />
      <StatsGrid stats={dashboardStats} />
    </DashboardLayout>
  )
}

export default App