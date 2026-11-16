import { useEffect, useState } from 'react'
import { fetchCategories, fetchJobs } from './api.js'
import Filters from './components/Filters.jsx'
import JobCard from './components/JobCard.jsx'

const EMPTY_FILTERS = { search: '', category: '', location: '' }
const TYPING_DELAY_MS = 300

export default function App() {
  const [filters, setFilters] = useState(EMPTY_FILTERS)
  const [categories, setCategories] = useState([])
  const [jobs, setJobs] = useState([])
  const [total, setTotal] = useState(0)
  const [status, setStatus] = useState('loading') // 'loading' | 'ready' | 'error'
  const [loadingMore, setLoadingMore] = useState(false)

  useEffect(() => {
    // The dropdown still works with just "All categories" if this fails.
    fetchCategories()
      .then(setCategories)
      .catch(() => {})
  }, [])

  useEffect(() => {
    // Wait until typing pauses so we send one request instead of one per keystroke.
    // `ignore` drops answers to old filters that arrive after newer ones.
    let ignore = false
    const timer = setTimeout(async () => {
      try {
        const page = await fetchJobs({ ...filters, offset: 0 })
        if (ignore) return
        setJobs(page.items)
        setTotal(page.total)
        setStatus('ready')
      } catch {
        if (!ignore) setStatus('error')
      }
    }, TYPING_DELAY_MS)

    return () => {
      ignore = true
      clearTimeout(timer)
    }
  }, [filters])

  function changeFilters(nextFilters) {
    setFilters(nextFilters)
    setStatus('loading')
  }

  async function loadMore() {
    setLoadingMore(true)
    try {
      const page = await fetchJobs({ ...filters, offset: jobs.length })
      setJobs((previous) => [...previous, ...page.items])
    } catch {
      setStatus('error')
    } finally {
      setLoadingMore(false)
    }
  }

  return (
    <main className="page">
      <header className="header">
        <h1>Internship Board</h1>
        {status === 'ready' && <p className="count">{total.toLocaleString()} internships</p>}
      </header>

      <Filters filters={filters} categories={categories} onChange={changeFilters} />

      {status === 'loading' && <p className="message">Loading internships…</p>}

      {status === 'error' && (
        <p className="message error">Couldn't load internships. Is the API running?</p>
      )}

      {status === 'ready' && jobs.length === 0 && (
        <div className="message">
          <p>No internships match these filters.</p>
          <button type="button" onClick={() => changeFilters(EMPTY_FILTERS)}>
            Clear filters
          </button>
        </div>
      )}

      {status === 'ready' && (
        <section className="job-list">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </section>
      )}

      {status === 'ready' && jobs.length < total && (
        <button type="button" className="load-more" onClick={loadMore} disabled={loadingMore}>
          {loadingMore ? 'Loading…' : `Load more (${jobs.length} of ${total.toLocaleString()})`}
        </button>
      )}
    </main>
  )
}
