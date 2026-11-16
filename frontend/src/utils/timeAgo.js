const ONE_DAY_MS = 24 * 60 * 60 * 1000

// `now` is a parameter so tests can pin "today" instead of depending on the real clock.
export function timeAgo(isoDate, now = new Date()) {
  const days = Math.floor((now - new Date(isoDate)) / ONE_DAY_MS)

  if (days < 1) return 'today'
  if (days === 1) return '1 day ago'
  if (days < 30) return `${days} days ago`

  const months = Math.floor(days / 30)
  return months === 1 ? '1 month ago' : `${months} months ago`
}
