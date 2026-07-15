import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import LandingPage from './pages/LandingPage';
import QueryWorkspace from './pages/QueryWorkspace';
import AboutPage from './pages/AboutPage';
import { checkBackendHealth } from './services/api';

function App() {
  const [currentPage, setCurrentPage] = useState('landing');
  const [preloadedQuery, setPreloadedQuery] = useState('');
  const [backendHealthy, setBackendHealthy] = useState(false);

  // Check health of backend on mount
  useEffect(() => {
    const verifyHealth = async () => {
      const isHealthy = await checkBackendHealth();
      setBackendHealthy(isHealthy);
    };

    verifyHealth();

    // Check health every 15 seconds to keep track of connection status
    const interval = setInterval(verifyHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  const renderPage = () => {
    switch (currentPage) {
      case 'landing':
        return (
          <LandingPage 
            setCurrentPage={setCurrentPage} 
            setPreloadedQuery={setPreloadedQuery} 
          />
        );
      case 'query':
        return (
          <QueryWorkspace 
            preloadedQuery={preloadedQuery} 
            setPreloadedQuery={setPreloadedQuery} 
          />
        );
      case 'about':
        return <AboutPage />;
      default:
        return <LandingPage setCurrentPage={setCurrentPage} setPreloadedQuery={setPreloadedQuery} />;
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-slate-950 text-slate-150">
      
      {/* Premium Navigation Header */}
      <Header 
        currentPage={currentPage} 
        setCurrentPage={setCurrentPage} 
        backendHealthy={backendHealthy} 
      />

      {/* Main Page Layout Renderer */}
      <main className="flex-1 w-full pb-12">
        {renderPage()}
      </main>

      {/* Premium Disclaimer Footer */}
      <Footer />
      
    </div>
  );
}

export default App;
