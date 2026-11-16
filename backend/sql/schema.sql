-- =============================================================
-- jobs: one row per internship listing.
-- Safe to run many times: "IF NOT EXISTS" skips what already exists.
-- =============================================================

CREATE TABLE IF NOT EXISTS jobs (
    -- Identity --------------------------------------------------
    id            TEXT PRIMARY KEY,        -- the source's unique id; blocks duplicates
    source        TEXT NOT NULL,           -- where the listing came from, e.g. 'Simplify'

    -- What the student sees ---------------------------------------
    company_name  TEXT NOT NULL,
    title         TEXT NOT NULL,
    category      TEXT,                    -- e.g. 'Software', 'Data Science'
    locations     TEXT[] NOT NULL DEFAULT '{}',  -- a job can have several locations
    url           TEXT NOT NULL,           -- the "Apply" link
    sponsorship   TEXT,                    -- visa sponsorship info, if given
    degrees       TEXT[] NOT NULL DEFAULT '{}',
    terms         TEXT[] NOT NULL DEFAULT '{}',  -- e.g. {'Summer 2027'}

    -- Status and dates --------------------------------------------
    active        BOOLEAN NOT NULL DEFAULT TRUE,  -- is the posting still open?
    date_posted   TIMESTAMPTZ NOT NULL,           -- when the company posted it
    date_updated  TIMESTAMPTZ,                    -- when the source last changed it

    -- Our own bookkeeping -----------------------------------------
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),  -- first time OUR fetcher saw it
    last_seen_at  TIMESTAMPTZ NOT NULL DEFAULT now()   -- most recent time we saw it
);

-- Indexes: like a book's index, so Postgres finds rows without reading all of them.
CREATE INDEX IF NOT EXISTS idx_jobs_date_posted ON jobs (date_posted DESC);  -- "most recent" sort
CREATE INDEX IF NOT EXISTS idx_jobs_category    ON jobs (category);          -- category filter

-- Security: lock the table for Supabase's public API roles (defense in depth).
-- Our backend connects as the table's owner, which is not affected.
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
