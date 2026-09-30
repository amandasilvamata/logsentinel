import { useRef, useState } from 'react'
import FileUpload from './components/FileUpload.jsx'
import AnalysisSummary from './components/AnalysisSummary.jsx'
import AlertList from './components/AlertList.jsx'

const API_URL = 'http://127.0.0.1:8000/analyze'

function App() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const resultsRef = useRef(null)

  function handleFileSelect(selectedFile) {
    if (!selectedFile || isAnalyzing) return
    setResult(null)
    if (!/\.(log|txt)$/.test(selectedFile.name)) {
      setFile(null)
      setError('Choose a .log or .txt file to continue.')
      return
    }
    if (selectedFile.size === 0) {
      setFile(null)
      setError('This file is empty. Choose a log with content.')
      return
    }
    setError('')
    setFile(selectedFile)
  }

  async function handleAnalyze() {
    if (!file || isAnalyzing) return
    setIsAnalyzing(true)
    setError('')
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(API_URL, { method: 'POST', body: formData })
      const payload = await response.json().catch(() => null)
      if (!response.ok) {
        const detail = typeof payload?.detail === 'string' ? payload.detail : 'The analysis could not be completed.'
        throw new Error(detail)
      }
      if (!payload?.file || !payload?.summary || !Array.isArray(payload?.alerts)) {
        throw new Error('The analysis server returned an unexpected response.')
      }
      setResult(payload)
      requestAnimationFrame(() => resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
    } catch (requestError) {
      setError(requestError instanceof TypeError
        ? 'Cannot reach the local analysis server. Start FastAPI at 127.0.0.1:8000 and try again.'
        : requestError.message)
    } finally {
      setIsAnalyzing(false)
    }
  }

  return <div className="site-shell" id="top">
    <header className="site-header">
      <a className="wordmark" href="#top" aria-label="LogSentinel, back to top">LS<span className="wordmark-mark">/</span></a>
      <span className="header-descriptor">LINUX SECURITY LOG ANALYZER <span>—</span> RELEASE 01</span>
      <a className="header-link" href="#analyze">OPEN ANALYZER <span aria-hidden="true">↗</span></a>
    </header>

    <main>
      <section className="hero" aria-labelledby="hero-title">
        <div className="hero-grid" aria-hidden="true"><span>AUTH / 001</span><span>INPUT → SIGNAL</span><span>RULESET / 03</span></div>
        <div className="hero-meta"><span>INDEPENDENT SECURITY UTILITY</span><span>01 — 03 / FIELD NOTES</span></div>
        <div className="hero-copy">
          <p className="system-status"><span className="status-dot" /> SYSTEM ONLINE <span className="status-divider">/</span> LOCAL ANALYSIS</p>
          <h1 id="hero-title"><span>LOG</span><span>SENTINEL<span className="hero-period">.</span></span></h1>
          <div className="hero-description">
            <p>Linux authentication log analysis for detecting suspicious access patterns.</p>
            <span>MAKE SENSE OF<br />WHAT HAPPENED.</span>
          </div>
        </div>
        <div className="hero-bottom">
          <a href="#analyze" className="hero-cta">START AN ANALYSIS <span aria-hidden="true">↘</span></a>
          <p>FROM RAW LOGS TO CLEAR SIGNALS.</p>
          <span>SCROLL TO EXPLORE ↓</span>
        </div>
      </section>

      <FileUpload file={file} onFileSelect={handleFileSelect} onAnalyze={handleAnalyze} isAnalyzing={isAnalyzing} error={error} />
      <div ref={resultsRef}>
        {result && <>
          <AnalysisSummary result={result} />
          <AlertList alerts={result.alerts} />
        </>}
      </div>
    </main>

    <footer className="site-footer">
      <span className="footer-brand">LogSentinel<span>.</span></span>
      <span>LINUX SECURITY LOG ANALYZER</span>
      <a href="#top">BACK TO TOP ↑</a>
    </footer>
  </div>
}

export default App
