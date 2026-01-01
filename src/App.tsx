import { useMockApp } from './lib/store';
import { Layout } from './components/layout/MainLayout';
import { ChatInterface } from './components/chat/ChatInterface';
import { Dashboard } from './components/dashboard/Dashboard';
import { LandingPage } from './components/landing/LandingPage';
import './index.css';

function App() {
  const { currentUser, switchRole, showLanding, matchRole } = useMockApp();

  if (showLanding) {
    return <LandingPage onLogin={matchRole} />;
  }

  return (
    <Layout user={currentUser} onSwitchRole={switchRole}>
      {currentUser.role === 'client' ? (
        <ChatInterface />
      ) : (
        <Dashboard />
      )}
    </Layout>
  );
}

export default App;
