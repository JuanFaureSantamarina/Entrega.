from datetime import date as _date

from .db import get_connection
from .transactions import list_movements


def set_budget(category: str, amount: float, month: str = None) -> int:
    if amount <= 0:
        raise ValueError("El monto debe ser mayor a 0")
    month = month or _date.today().strftime("%Y-%m")

    conn = get_connection()
    conn.execute(
        """INSERT INTO budgets (category, month, amount) VALUES (?, ?, ?)
           ON CONFLICT(category, month) DO UPDATE SET amount = excluded.amount""",
        (category, month, amount),
    )
    conn.commit()
    row = conn.execute(
        "SELECT id FROM budgets WHERE category = ? AND month = ?", (category, month)
    ).fetchone()
    conn.close()
    return row["id"]


def list_budgets(month: str = None) -> list:
    month = month or _date.today().strftime("%Y-%m")
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM budgets WHERE month = ? ORDER BY category", (month,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def budget_status(month: str = None) -> list:
    """For each budgeted category in the month, compare against actual spend."""
    month = month or _date.today().strftime("%Y-%m")
    budgets = list_budgets(month)
    expenses = list_movements(month=month, type_="expense")

    spent_by_category = {}
    for e in expenses:
        spent_by_category[e["category"]] = spent_by_category.get(e["category"], 0) + e["amount"]

    result = []
    for b in budgets:
        spent = spent_by_category.get(b["category"], 0)
        result.append({
            "category": b["category"],
            "budget": b["amount"],
            "spent": spent,
            "remaining": b["amount"] - spent,
            "pct_used": round((spent / b["amount"]) * 100, 1) if b["amount"] else 0,
        })
    return result


def delete_budget(category: str, month: str) -> bool:
    conn = get_connection()
    cur = conn.execute("DELETE FROM budgets WHERE category = ? AND month = ?", (category, month))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted
