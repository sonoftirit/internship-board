# Internship Board

[![CI](https://github.com/sonoftirit/internship-board/actions/workflows/ci.yml/badge.svg)](https://github.com/sonoftirit/internship-board/actions/workflows/ci.yml)

A job board for CS students: it pulls internship listings from the
[SimplifyJobs](https://github.com/SimplifyJobs/Summer2027-Internships) list, stores them
in PostgreSQL, and shows them on a dashboard with filters and an **Apply** link.

- **Live demo:** https://internship-board-rosy.vercel.app
- **API docs:** https://internship-board-api-e51q.onrender.com/docs

> The API runs on a free plan that sleeps when idle, so the first load can take up to a minute.

## Features

- Thousands of active internships, newest first
- Search by company or title, filter by category and location
- "Posted 3 days ago" dates, **Apply** opens the original posting
- Load more (pagination)

## Architecture

```
SimplifyJobs JSON ──(ingest.py: fetch → validate → upsert)──▶ PostgreSQL (Supabase)
                                                                    ▲
                                                                    │ SQL
React dashboard (Vercel) ──HTTPS GET /api/jobs?search=&category=──▶ FastAPI (Render)
```

Every pull request runs lint, tests and a production build in GitHub Actions.
Merging to `main` deploys the API (Render) and the dashboard (Vercel) automatically.

## Tech stack

| Layer    | Tech                                                    |
|----------|---------------------------------------------------------|
| Data     | PostgreSQL (Supabase), psycopg                           |
| Backend  | Python, FastAPI, Pydantic                                |
| Frontend | React + Vite, plain CSS                                  |
| Quality  | pytest, Ruff, Vitest, oxlint, GitHub Actions (CI)        |
| Hosting  | Render (API), Vercel (dashboard), Supabase (database)    |

## API

| Endpoint | Description |
|---|---|
| `GET /health` | Liveness check |
| `GET /api/jobs?search=&category=&location=&limit=50&offset=0` | Active jobs, newest first, with the total count |
| `GET /api/categories` | Categories for the filter dropdown |

## Run it locally

**Backend** (Python 3.14):

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env            # then put your real DATABASE_URL in .env
python -m app.ingest            # load listings into the database
uvicorn app.main:app --reload   # http://localhost:8000/docs
```

**Frontend** (Node 24), in a second terminal:

```bash
cd frontend
npm install
npm run dev                     # http://localhost:5173
```

**Tests and checks:**

```bash
cd backend && ruff check . && pytest
cd frontend && npm run lint && npm test
```

## Roadmap

- **P0** fetch → store → dashboard → filters → Apply → CI → deploy ✅
- **P1** daily scheduled ingest, move backend to AWS
- **P2** user accounts + application tracker
- **P3** AI resume tailoring per job description
- **P4** DSA interview practice with an AI assistant
