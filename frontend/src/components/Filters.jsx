export default function Filters({ filters, categories, onChange }) {
  function update(field) {
    return (event) => onChange({ ...filters, [field]: event.target.value })
  }

  return (
    <div className="filters">
      <input
        type="search"
        placeholder="Search company or title"
        aria-label="Search company or title"
        value={filters.search}
        onChange={update('search')}
      />
      <select aria-label="Category" value={filters.category} onChange={update('category')}>
        <option value="">All categories</option>
        {categories.map((category) => (
          <option key={category} value={category}>
            {category}
          </option>
        ))}
      </select>
      <input
        type="search"
        placeholder="Location (e.g. Remote, NYC)"
        aria-label="Location"
        value={filters.location}
        onChange={update('location')}
      />
    </div>
  )
}
