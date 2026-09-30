export function formatBytes(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

export function formatCount(value) {
  return new Intl.NumberFormat('en-US').format(value ?? 0)
}

export function formatAlertType(type) {
  const names = {
    brute_force: 'Brute Force Activity',
    root_attack: 'Root Account Targeting',
    success_after_failures: 'Successful Login After Failures',
  }
  return names[type] || String(type || 'Unknown Alert')
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

export function formatTimestamp(value) {
  if (!value) return ''
  return String(value).replace('T', ' ').replace('Z', ' UTC')
}
