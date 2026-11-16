import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# Load backend/.env no matter which folder the program is started from.
# On the deployed server there is no .env file; the host sets DATABASE_URL directly.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def get_connection() -> psycopg.Connection:
    """Open a new connection to the Postgres database."""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set. Copy backend/.env.example to backend/.env.")
    return psycopg.connect(url)
