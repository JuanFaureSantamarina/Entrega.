import sqlite3
import os
from datetime import datetime
from pathlib import Path


DB_PATH = Path("data/applications.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                niche TEXT NOT NULL,
                status TEXT DEFAULT 'enviada',
                applied_at TEXT NOT NULL,
                cv_path TEXT,
                cover_letter_path TEXT,
                job_url TEXT,
                contact_email TEXT,
                notes TEXT,
                updated_at TEXT NOT NULL
            )
        """)
        conn.commit()


def add_application(company, position, niche, cv_path=None, cover_letter_path=None,
                    job_url=None, contact_email=None, notes=None):
    init_db()
    now = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO applications
            (company, position, niche, applied_at, cv_path, cover_letter_path,
             job_url, contact_email, notes, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (company, position, niche, now, cv_path, cover_letter_path,
              job_url, contact_email, notes, now))
        conn.commit()
        return cursor.lastrowid


def update_status(app_id, status, notes=None):
    init_db()
    now = datetime.now().isoformat()
    with get_connection() as conn:
        if notes:
            conn.execute(
                "UPDATE applications SET status=?, notes=?, updated_at=? WHERE id=?",
                (status, notes, now, app_id)
            )
        else:
            conn.execute(
                "UPDATE applications SET status=?, updated_at=? WHERE id=?",
                (status, now, app_id)
            )
        conn.commit()


def list_applications(niche=None, status=None):
    init_db()
    query = "SELECT * FROM applications WHERE 1=1"
    params = []
    if niche:
        query += " AND niche=?"
        params.append(niche)
    if status:
        query += " AND status=?"
        params.append(status)
    query += " ORDER BY applied_at DESC"
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query, params).fetchall()
    return [dict(r) for r in rows]


def get_stats():
    init_db()
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        total = conn.execute("SELECT COUNT(*) as c FROM applications").fetchone()["c"]
        by_status = conn.execute(
            "SELECT status, COUNT(*) as c FROM applications GROUP BY status"
        ).fetchall()
        by_niche = conn.execute(
            "SELECT niche, COUNT(*) as c FROM applications GROUP BY niche"
        ).fetchall()
    return {
        "total": total,
        "by_status": {r["status"]: r["c"] for r in by_status},
        "by_niche": {r["niche"]: r["c"] for r in by_niche},
    }
