import AlertRow from './AlertRow.jsx'

function AlertList({ alerts, eventsFound }) {
  const hasAlerts = alerts.length > 0
  return <section className="alerts-section" aria-labelledby="alerts-title">
    <div className="section-bar"><span>03 / INCIDENT REGISTER</span><span>{String(alerts.length).padStart(2, '0')} SIGNALS</span></div>
    <div className="alerts-heading">
      <p className="section-eyebrow">DETECTION OUTPUT / SORTED BY SEVERITY</p>
      <h2 id="alerts-title">{eventsFound === 0 ? <>No events<br /><em>recognized.</em></> : hasAlerts ? <>Security<br /><em>alerts.</em></> : <>No threats<br /><em>detected.</em></>}</h2>
      <p>{eventsFound === 0 ? 'No supported authentication events were recognized. Check the log format.' : hasAlerts ? 'A closer look at the suspicious activity found in this file.' : 'No detection rules matched this file. Review the source if you expected an alert.'}</p>
    </div>
    {hasAlerts && <ol className="alert-list">{[...alerts]
      .sort((a, b) => ({ critical: 3, high: 2, medium: 1 }[b.severity] || 0) - ({ critical: 3, high: 2, medium: 1 }[a.severity] || 0))
      .map((alert, index) => <AlertRow key={index} alert={alert} index={index} />)}</ol>}
  </section>
}

export default AlertList
