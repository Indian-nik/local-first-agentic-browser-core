import React, { useState, useEffect } from 'react';
import './App.css';
import HomePage from './pages/HomePage';
import ComponentsPage from './pages/ComponentsPage';
import PlaygroundPage from './pages/PlaygroundPage';
import ThemeEditorPage from './pages/ThemeEditorPage';
import DocsPage from './pages/DocsPage';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [theme, setTheme] = useState('ocean');
  const [appVersion, setAppVersion] = useState('');

  useEffect(() => {
    // Get app version
    window.electron?.getAppVersion().then(version => {
      setAppVersion(version);
    });

    // Listen for updates
    window.electron?.onUpdateAvailable(() => {
      console.log('Update available');
    });

    window.electron?.onUpdateDownloaded(() => {
      const install = window.confirm('Update downloaded. Install now?');
      if (install) {
        window.electron.installUpdate();
      }
    });
  }, []);

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage onNavigate={setCurrentPage} />;
      case 'components':
        return <ComponentsPage />;
      case 'playground':
        return <PlaygroundPage />;
      case 'theme-editor':
        return <ThemeEditorPage theme={theme} setTheme={setTheme} />;
      case 'docs':
        return <DocsPage />;
      default:
        return <HomePage onNavigate={setCurrentPage} />;
    }
  };

  return (
    <div className="conda-app" data-theme={theme}>
      <nav className="conda-nav">
        <div className="conda-nav-brand">
          <span className="conda-logo">🐍</span>
          <span>CONDA Design System</span>
        </div>
        <div className="conda-nav-items">
          <button 
            className={currentPage === 'home' ? 'active' : ''}
            onClick={() => setCurrentPage('home')}
          >
            Home
          </button>
          <button 
            className={currentPage === 'components' ? 'active' : ''}
            onClick={() => setCurrentPage('components')}
          >
            Components
          </button>
          <button 
            className={currentPage === 'playground' ? 'active' : ''}
            onClick={() => setCurrentPage('playground')}
          >
            Playground
          </button>
          <button 
            className={currentPage === 'theme-editor' ? 'active' : ''}
            onClick={() => setCurrentPage('theme-editor')}
          >
            Theme Editor
          </button>
          <button 
            className={currentPage === 'docs' ? 'active' : ''}
            onClick={() => setCurrentPage('docs')}
          >
            Docs
          </button>
        </div>
        <div className="conda-nav-info">
          <span className="version">v{appVersion}</span>
        </div>
      </nav>
      <main className="conda-main">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;
