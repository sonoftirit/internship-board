"""SQL used by the API.

User input only ever travels through %(name)s placeholders, never inside the SQL text,
so it can't change what the query does (SQL injection).
"""

from psycopg.rows import dict_row

JOB_COLUMNS = "id, company_name, title, category, locations, url, sponsorship, date_posted"


def build_filters(
    search: str | None, category: str | None, location: str | None
) -> tuple[str, dict]:
    """Turn the optional filters into a WHERE clause (fixed text) and its parameter values."""
    conditions = ["active"]
    params = {}
    if search:
        conditions.append("(company_name ILIKE %(search)s OR title ILIKE %(search)s)")
        params["search"] = f"%{search}%"
    if category:
        conditions.append("category = %(category)s")
        params["category"] = category
    if location:
        conditions.append("array_to_string(locations, ' ') ILIKE %(location)s")
        params["location"] = f"%{location}%"
    return " AND ".join(conditions), params


def list_jobs(
    conn,
    search: str | None = None,
    category: str | None = None,
    location: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[int, list[dict]]:
    """Return (total matching jobs, one page of jobs), newest first."""
    where, params = build_filters(search, category, location)
    with conn.cursor(row_factory=dict_row) as cur:
        total = cur.execute(f"SELECT count(*) AS n FROM jobs WHERE {where}", params).fetchone()["n"]
        cur.execute(
            f"SELECT {JOB_COLUMNS} FROM jobs WHERE {where} "
            "ORDER BY date_posted DESC, id "  # id breaks ties so pages never overlap
            "LIMIT %(limit)s OFFSET %(offset)s",
            {**params, "limit": limit, "offset": offset},
        )
        rows = cur.fetchall()
    return total, rows


def list_categories(conn) -> list[str]:
    """Distinct categories of active jobs, for the dashboard's dropdown."""
    rows = conn.execute(
        "SELECT DISTINCT category FROM jobs WHERE active AND category IS NOT NULL ORDER BY category"
    ).fetchall()
    return [row[0] for row in rows]
