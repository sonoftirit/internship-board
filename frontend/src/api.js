// The only file that talks to the backend; components never call fetch directly.
const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

async function getJson(path, params = {}) {
  const url = new URL(path, API_URL)
  for (const [key, value] of Object.entries(params)) {
    if (value !== '' && value !== undefined && value !== null) {
      url.searchParams.set(key, value)
    }
  }
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`)
  }
  return response.json()
}

export function fetchJobs({ search, category, location, offset = 0, limit = 30 }) {
  return getJson('/api/jobs', { search, category, location, offset, limit })
}

export function fetchCategories() {
  return getJson('/api/categories')
}
