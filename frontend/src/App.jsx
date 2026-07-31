import { useEffect, useState } from 'react'
import { getHealth } from './api/client'
import './App.css'

function App() {
  const [health, setHealth] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    getHealth()
      .then((data) => setHealth(data))
      .catch((err) => setError(err.message))
  }, [])

  return (
    <div className="app">
      <header className="app-header">
        <h1>🛡️ CyberRakshak AI</h1>
        <p>AI-powered cyber threat detection and response</p>
      </header>

      <main className="app-main">
        <section className="status-card">
          <h2>Backend Status</h2>
          {error ? (
            <p className="status-error">
              Unable to reach backend: {error}
            </p>
          ) : health ? (
            <div className="status-ok">
              <p>
                Service: <strong>{health.service}</strong>
              </p>
              <p>
                Status: <strong>{health.status}</strong>
              </p>
              <p>
                Version: <strong>{health.version}</strong>
              </p>
            </div>
          ) : (
            <p>Loading backend status…</p>
          )}
        </section>

        <section className="info-grid">
          <div className="info-card">
            <h3>🚀 Getting Started</h3>
            <p>Check the README for setup instructions.</p>
          </div>
          <div className="info-card">
            <h3>📚 API Docs</h3>
            <p>
              Interactive Swagger docs at{' '}
              <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer">
                /docs
              </a>
            </p>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
