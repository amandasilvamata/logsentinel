import { formatCount } from '../utils/format.js'

function AnalysisSummary({ result }) {
  const severity = result.summary?.severity || {}
  const metrics = [
    ['HIGH', severity.high],
    ['CRITICAL', severity.critical],
    ['MEDIUM', severity.medium],
  ]

  return <section className="summary-section" id="results" aria-labelledby="summary-title">
    <div className="section-bar"><span>02 / FINDINGS</span><span>ANALYSIS COMPLETE</span></div>
    <div className="summary-heading">
      <div>
        <p className="section-eyebrow">SOURCE / {result.file?.name || 'UNKNOWN FILE'}</p>
        <h2 id="summary-title">The<br />readout<span>.</span></h2>
      </div>
      <p>Authentication activity, distilled into the signals that need attention.</p>
    </div>
    <div className="primary-metrics">
      <div className="primary-metric">
        <span>01 / EVENTS FOUND</span>
        <strong>{formatCount(result.file?.events_found)}</strong>
        <small>PARSED AUTHENTICATION EVENTS</small>
      </div>
      <div className="primary-metric">
        <span>02 / ALERTS FOUND</span>
        <strong>{formatCount(result.summary?.alerts_found)}</strong>
        <small>DETECTION RULE MATCHES</small>
      </div>
    </div>
    <div className="severity-metrics" aria-label="Alerts by severity">
      {metrics.map(([label, count], index) => <div className={'severity-metric ' + label.toLowerCase()} key={label}>
        <span>0{index + 3} / {label}</span>
        <strong>{formatCount(count)}</strong>
      </div>)}
    </div>
  </section>
}

export default AnalysisSummary
