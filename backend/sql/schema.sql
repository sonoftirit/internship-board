-- One row per internship listing. Safe to re-run (IF NOT EXISTS).
CREATE TABLE IF NOT EXISTS jobs (
    id            TEXT PRIMARY KEY,               -- source's id; prevents duplicate listings
    source        TEXT NOT NULL,
    company_name  TEXT NOT NULL,
    title         TEXT NOT NULL,
    category      TEXT,
    locations     TEXT[] NOT NULL DEFAULT '{}',
    url           TEXT NOT NULL,
    sponsorship   TEXT,
    degrees       TEXT[] NOT NULL DEFAULT '{}',
    terms         TEXT[] NOT NULL DEFAULT '{}',
    active        BOOLEAN NOT NULL DEFAULT TRUE,
    date_posted   TIMESTAMPTZ NOT NULL,
    date_updated  TIMESTAMPTZ,
    -- Our own bookkeeping, separate from the source's dates
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_jobs_date_posted ON jobs (date_posted DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_category    ON jobs (category);

-- Blocks Supabase's public API roles; the backend connects as owner and is unaffected.
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
