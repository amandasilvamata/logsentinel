import { formatAlertType, formatTimestamp } from '../utils/format.js'

function AlertRow({ alert, index }) {
  const severity = String(alert.severity || 'unknown').toLowerCase()
  const details = [
    alert.ip && ['SOURCE IP', alert.ip],
    alert.user && ['USER', alert.user],
    alert.attempts != null && ['ATTEMPTS', alert.attempts],
    alert.failed_attempts != null && ['FAILED ATTEMPTS', alert.failed_attempts],
    alert.time_window != null && ['TIME WINDOW', alert.time_window + ' s'],
    alert.timestamp && ['TIMESTAMP', formatTimestamp(alert.timestamp)],
  ].filter(Boolean)

  return <li className={'alert-row ' + (severity === 'critical' ? 'is-critical' : '')}>
    <div className="alert-index">{String(index + 1).padStart(2, '0')}</div>
    <div className="alert-main">
      <div className="alert-topline"><span className={'alert-severity severity-' + severity}>{severity.toUpperCase()}</span><span>DETECTION / {alert.type || 'unknown'}</span></div>
      <h3>{formatAlertType(alert.type)}</h3>
      <div className="alert-details">{details.map(([label, value]) => <div key={label}><span>{label}</span><strong>{value}</strong></div>)}</div>
    </div>
    <span className="alert-arrow" aria-hidden="true">↗</span>
  </li>
}

export default AlertRow
