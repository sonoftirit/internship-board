import { timeAgo } from '../utils/timeAgo.js'

const MAX_LOCATIONS = 3

function formatLocations(locations) {
  if (locations.length === 0) return 'Location not listed'
  const shown = locations.slice(0, MAX_LOCATIONS).join(' · ')
  const hidden = locations.length - MAX_LOCATIONS
  return hidden > 0 ? `${shown} +${hidden} more` : shown
}

export default function JobCard({ job }) {
  return (
    <article className="job-card">
      <div className="job-main">
        <p className="company">{job.company_name}</p>
        <h2 className="title">{job.title}</h2>
        <p className="locations">{formatLocations(job.locations)}</p>
      </div>
      <div className="job-side">
        <span className="posted">{timeAgo(job.date_posted)}</span>
        {job.category && <span className="tag">{job.category}</span>}
        {/* noopener: the job site can't control our tab; noreferrer: it isn't told where the click came from */}
        <a className="apply" href={job.url} target="_blank" rel="noopener noreferrer">
          Apply ↗
        </a>
      </div>
    </article>
  )
}
