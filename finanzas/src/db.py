import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "finanzas.db"

TURSO_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

SCHEMA = """
CREATE TABLE IF NOT EXISTS movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    due_date TEXT NOT NULL,
    recurring TEXT NOT NULL DEFAULT 'none' CHECK(recurring IN ('none', 'weekly', 'monthly', 'yearly')),
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'paid')),
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    month TEXT NOT NULL,
    amount REAL NOT NULL,
    UNIQUE(category, month)
);
"""


class _TursoRow(dict):
    """Dict subclass so `dict(row)` and `row['col']` both behave like sqlite3.Row."""


class _TursoCursor:
    def __init__(self, result_set):
        cols = list(getattr(result_set, "columns", []) or [])
        self._rows = [_TursoRow(zip(cols, row)) for row in getattr(result_set, "rows", [])]
        self.rowcount = getattr(result_set, "rows_affected", -1)
        self.lastrowid = getattr(result_set, "last_insert_rowid", None)
        self._pos = 0

    def fetchall(self):
        return list(self._rows)

    def fetchone(self):
        if self._pos >= len(self._rows):
            return None
        row = self._rows[self._pos]
        self._pos += 1
        return row


class _TursoConnection:
    """Minimal shim exposing the sqlite3.Connection surface this app uses,
    backed by a remote libSQL (Turso) database over HTTP."""

    def __init__(self, client):
        self._client = client

    def execute(self, sql, params=()):
        rs = self._client.execute(sql, list(params))
        return _TursoCursor(rs)

    def executescript(self, script):
        for stmt in [s.strip() for s in script.split(";") if s.strip()]:
            self._client.execute(stmt)

    def commit(self):
        pass  # each statement is committed server-side as it executes

    def close(self):
        self._client.close()


def _turso_connection():
    import libsql_client
    client = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)
    conn = _TursoConnection(client)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_connection():
    if TURSO_URL and TURSO_TOKEN:
        return _turso_connection()

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
