from datetime import date as _date

from .db import get_connection


def add_movement(type_: str, amount: float, category: str, description: str = "", date: str = None) -> int:
    if type_ not in ("income", "expense"):
        raise ValueError("type debe ser 'income' o 'expense'")
    if amount <= 0:
        raise ValueError("El monto debe ser mayor a 0")
    date = date or _date.today().isoformat()

    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO movements (type, amount, category, description, date) VALUES (?, ?, ?, ?, ?) RETURNING id",
        (type_, amount, category, description, date),
    )
    movement_id = cur.fetchone()["id"]
    conn.commit()
    conn.close()
    return movement_id


def list_movements(month: str = None, type_: str = None, category: str = None) -> list:
    query = "SELECT * FROM movements WHERE 1=1"
    params = []
    if month:
        query += " AND date LIKE ?"
        params.append(f"{month}%")
    if type_:
        query += " AND type = ?"
        params.append(type_)
    if category:
        query += " AND category = ?"
        params.append(category)
    query += " ORDER BY date DESC, id DESC"

    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_movement(movement_id: int) -> bool:
    conn = get_connection()
    cur = conn.execute("DELETE FROM movements WHERE id = ?", (movement_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted


def get_movement(movement_id: int) -> dict:
    conn = get_connection()
    row = conn.execute("SELECT * FROM movements WHERE id = ?", (movement_id,)).fetchone()
    conn.close()
    return dict(row) if row else None
