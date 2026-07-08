import calendar
from datetime import date as _date, datetime, timedelta

from .db import get_connection
from .transactions import add_movement


def _add_period(due_date: _date, recurring: str) -> _date:
    if recurring == "weekly":
        return due_date + timedelta(days=7)
    if recurring == "monthly":
        month = due_date.month + 1
        year = due_date.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        day = min(due_date.day, calendar.monthrange(year, month)[1])
        return _date(year, month, day)
    if recurring == "yearly":
        try:
            return due_date.replace(year=due_date.year + 1)
        except ValueError:
            # Feb 29 on a non-leap year
            return due_date.replace(year=due_date.year + 1, day=28)
    return due_date


def add_bill(name: str, amount: float, category: str, due_date: str, recurring: str = "none", notes: str = "") -> int:
    if amount <= 0:
        raise ValueError("El monto debe ser mayor a 0")
    if recurring not in ("none", "weekly", "monthly", "yearly"):
        raise ValueError("recurring debe ser: none, weekly, monthly o yearly")
    # Validate the date parses
    datetime.strptime(due_date, "%Y-%m-%d")

    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO bills (name, amount, category, due_date, recurring, notes) VALUES (?, ?, ?, ?, ?, ?)",
        (name, amount, category, due_date, recurring, notes),
    )
    conn.commit()
    bill_id = cur.lastrowid
    conn.close()
    return bill_id


def _classify(bill: dict, today: _date, soon_days: int = 7) -> str:
    if bill["status"] == "paid" and bill["recurring"] == "none":
        return "paid"
    due = datetime.strptime(bill["due_date"], "%Y-%m-%d").date()
    if due < today:
        return "overdue"
    if (due - today).days <= soon_days:
        return "due_soon"
    return "upcoming"


def list_bills(status: str = None, soon_days: int = 7) -> list:
    """status: pending, paid, overdue, due_soon, upcoming, or None for all pending+overdue+due_soon+upcoming"""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM bills ORDER BY due_date ASC").fetchall()
    conn.close()

    today = _date.today()
    bills = []
    for row in rows:
        b = dict(row)
        b["computed_status"] = _classify(b, today, soon_days)
        bills.append(b)

    if status == "all":
        return bills
    if status:
        return [b for b in bills if b["computed_status"] == status or (status == "pending" and b["status"] == "pending")]
    # default: everything not settled (paid, one-off)
    return [b for b in bills if b["computed_status"] != "paid"]


def get_bill(bill_id: int) -> dict:
    conn = get_connection()
    row = conn.execute("SELECT * FROM bills WHERE id = ?", (bill_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def pay_bill(bill_id: int, paid_date: str = None) -> dict:
    bill = get_bill(bill_id)
    if not bill:
        raise ValueError(f"No existe el vencimiento con id {bill_id}")

    paid_date = paid_date or _date.today().isoformat()

    # Register the payment as an expense movement
    add_movement(
        type_="expense",
        amount=bill["amount"],
        category=bill["category"],
        description=f"Pago: {bill['name']}",
        date=paid_date,
    )

    conn = get_connection()
    if bill["recurring"] == "none":
        conn.execute("UPDATE bills SET status = 'paid' WHERE id = ?", (bill_id,))
    else:
        due = datetime.strptime(bill["due_date"], "%Y-%m-%d").date()
        next_due = _add_period(due, bill["recurring"])
        conn.execute(
            "UPDATE bills SET due_date = ?, status = 'pending' WHERE id = ?",
            (next_due.isoformat(), bill_id),
        )
    conn.commit()
    conn.close()
    return get_bill(bill_id)


def delete_bill(bill_id: int) -> bool:
    conn = get_connection()
    cur = conn.execute("DELETE FROM bills WHERE id = ?", (bill_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted
