# Internship Board

A job board for CS students: it pulls internship listings from the
[SimplifyJobs](https://github.com/SimplifyJobs/Summer2027-Internships) list, stores them
in PostgreSQL, and shows them on a dashboard with filters and an **Apply** link.

> **Status:** P0 / MVP in progress.

## Architecture

```
SimplifyJobs JSON ──(ingest.py: fetch → validate → upsert)──▶ PostgreSQL (Supabase)
                                                                    │ SQL
React dashboard ──HTTP GET /api/jobs?search=&category=──▶ FastAPI ──┘
```

## Tech stack

| Layer    | Tech                          |
|----------|-------------------------------|
| Data     | PostgreSQL (Supabase), psycopg |
| Backend  | Python, FastAPI, Pydantic     |
| Frontend | React + Vite                  |
| Quality  | pytest, Ruff, GitHub Actions  |

## Run it locally

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env        # then put your real DATABASE_URL in .env
```

## Roadmap

- **P0** fetch → store → dashboard → filters → Apply
- **P1** daily scheduled ingest, move backend to AWS
- **P2** user accounts + application tracker
- **P3** AI resume tailoring per job description
- **P4** DSA interview practice with an AI assistant
