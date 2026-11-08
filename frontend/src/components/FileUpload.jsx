import { useRef, useState } from 'react'
import { formatBytes } from '../utils/format.js'

function FileUpload({ file, onFileSelect, onAnalyze, isAnalyzing, error }) {
  const inputRef = useRef(null)
  const dragDepth = useRef(0)
  const [isDragging, setIsDragging] = useState(false)

  function handleDragEnter(event) {
    event.preventDefault()
    dragDepth.current += 1
    setIsDragging(true)
  }

  function handleDragLeave(event) {
    event.preventDefault()
    dragDepth.current -= 1
    if (dragDepth.current <= 0) {
      dragDepth.current = 0
      setIsDragging(false)
    }
  }

  function handleDrop(event) {
    event.preventDefault()
    dragDepth.current = 0
    setIsDragging(false)
    onFileSelect(event.dataTransfer.files?.[0] || null)
  }

  function handleInputChange(event) {
    onFileSelect(event.target.files?.[0] || null)
    // Let the same file be selected again after a failed request.
    event.target.value = ''
  }

  return <section className="upload-section" id="analyze" aria-labelledby="upload-title">
    <div className="section-bar"><span>01 / INPUT</span><span>ANALYSIS TERMINAL</span></div>
    <div className="upload-layout">
      <div className="upload-intro">
        <p className="section-eyebrow">SOURCE MATERIAL / AUTHENTICATION LOGS</p>
        <h2 id="upload-title">Find the<br /><em>signal.</em></h2>
        <p>Drop a Linux authentication log. LogSentinel will scan for repeated failures, root account targeting, and successful access after failed attempts.</p>
        <span className="upload-aside">ONE FILE AT A TIME <span aria-hidden="true">↘</span></span>
      </div>
      <div className="upload-workspace">
        <div
          className={'dropzone' + (isDragging ? ' is-dragging' : '')}
          onDragEnter={handleDragEnter}
          onDragOver={(event) => event.preventDefault()}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input
            ref={inputRef}
            id="log-file"
            className="visually-hidden"
            type="file"
            disabled={isAnalyzing}
            accept=".log,.txt"
            onChange={handleInputChange}
            aria-describedby="upload-requirements"
          />
          <label htmlFor="log-file" className="dropzone-label">
            <span className="dropzone-arrow" aria-hidden="true">↗</span>
            <span className="dropzone-title">{file ? 'Source ready.' : 'Drop your log here.'}</span>
            <span className="dropzone-instruction">{file ? 'Choose another file' : 'or click to browse files'}</span>
          </label>
        </div>
        <div className="file-register">
          <div><span>FILE</span><strong title={file?.name}>{file?.name || 'No file selected'}</strong></div>
          <div><span>SIZE</span><strong>{file ? formatBytes(file.size) : '—'}</strong></div>
          <div><span>FORMAT</span><strong id="upload-requirements">.LOG / .TXT · MAX 10 MB</strong></div>
        </div>
        <div className="upload-action-row">
          <p>Files are sent to the analysis server.</p>
          <button type="button" className="analyze-button" onClick={onAnalyze} disabled={!file || isAnalyzing}>
            {isAnalyzing ? 'ANALYZING…' : 'ANALYZE FILE'} <span aria-hidden="true">↗</span>
          </button>
        </div>
        {error && <p className="upload-error" role="alert">{error}</p>}
        {isAnalyzing && <p className="upload-progress" role="status">Reading source and correlating events…</p>}
      </div>
    </div>
  </section>
}

export default FileUpload
