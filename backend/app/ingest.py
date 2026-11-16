"""Fetch internship listings, validate them, and upsert them into the jobs table.

Run from the backend folder:  python -m app.ingest
"""

import requests
from pydantic import ValidationError

from app.db import get_connection
from app.models import Listing

SOURCE_URL = (
    "https://raw.githubusercontent.com/SimplifyJobs/Summer2027-Internships"
    "/dev/.github/scripts/listings.json"
)

# Insert a job; if a row with the same id already exists, update it instead.
# That makes the pipeline idempotent: running it twice never creates duplicates.
UPSERT_SQL = """
INSERT INTO jobs (id, source, company_name, title, category, locations, url,
                  sponsorship, degrees, terms, active, date_posted, date_updated)
VALUES (%(id)s, %(source)s, %(company_name)s, %(title)s, %(category)s, %(locations)s, %(url)s,
        %(sponsorship)s, %(degrees)s, %(terms)s, %(active)s, %(date_posted)s, %(date_updated)s)
ON CONFLICT (id) DO UPDATE SET
    company_name = EXCLUDED.company_name,
    title        = EXCLUDED.title,
    category     = EXCLUDED.category,
    locations    = EXCLUDED.locations,
    url          = EXCLUDED.url,
    sponsorship  = EXCLUDED.sponsorship,
    degrees      = EXCLUDED.degrees,
    terms        = EXCLUDED.terms,
    active       = EXCLUDED.active,
    date_posted  = EXCLUDED.date_posted,
    date_updated = EXCLUDED.date_updated,
    last_seen_at = now()
"""


def fetch_listings(url: str = SOURCE_URL) -> list[dict]:
    """EXTRACT: download the raw listings (a list of dicts)."""
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.json()


def validate_listings(raw_listings: list[dict]) -> tuple[list[Listing], dict[str, int]]:
    """TRANSFORM: keep valid, visible listings and count what was skipped and why."""
    valid = []
    skipped = {"hidden": 0, "invalid": 0}
    for item in raw_listings:
        if not item.get("is_visible", True):
            skipped["hidden"] += 1
            continue
        try:
            valid.append(Listing.model_validate(item))
        except ValidationError:
            skipped["invalid"] += 1
    return valid, skipped


def upsert_jobs(conn, listings: list[Listing]) -> int:
    """LOAD: write all listings in one batch."""
    rows = [listing.model_dump(exclude={"is_visible"}) for listing in listings]
    with conn.cursor() as cur:
        cur.executemany(UPSERT_SQL, rows)
    conn.commit()
    return len(rows)


def main() -> None:
    raw = fetch_listings()
    listings, skipped = validate_listings(raw)
    with get_connection() as conn:
        saved = upsert_jobs(conn, listings)
        total = conn.execute("SELECT count(*) FROM jobs").fetchone()[0]

    print(f"fetched:  {len(raw)}")
    print(f"valid:    {len(listings)}")
    print(f"skipped:  {skipped}")
    print(f"saved:    {saved}")
    print(f"rows in jobs table: {total}")


if __name__ == "__main__":
    main()
