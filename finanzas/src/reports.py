from datetime import date as _date

from .transactions import list_movements
from .bills import list_bills
from .budgets import budget_status


def monthly_summary(month: str = None) -> dict:
    month = month or _date.today().strftime("%Y-%m")
    movements = list_movements(month=month)

    income_total = sum(m["amount"] for m in movements if m["type"] == "income")
    expense_total = sum(m["amount"] for m in movements if m["type"] == "expense")

    by_category = {}
    for m in movements:
        if m["type"] != "expense":
            continue
        by_category[m["category"]] = by_category.get(m["category"], 0) + m["amount"]

    return {
        "month": month,
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": income_total - expense_total,
        "expense_by_category": dict(sorted(by_category.items(), key=lambda x: -x[1])),
        "movement_count": len(movements),
    }


def overall_balance() -> float:
    movements = list_movements()
    income_total = sum(m["amount"] for m in movements if m["type"] == "income")
    expense_total = sum(m["amount"] for m in movements if m["type"] == "expense")
    return income_total - expense_total


def dashboard(soon_days: int = 7) -> dict:
    today = _date.today()
    month = today.strftime("%Y-%m")

    summary = monthly_summary(month)
    balance = overall_balance()

    overdue = list_bills(status="overdue", soon_days=soon_days)
    due_soon = list_bills(status="due_soon", soon_days=soon_days)

    budgets = budget_status(month)
    over_budget = [b for b in budgets if b["pct_used"] >= 100]
    near_budget = [b for b in budgets if 80 <= b["pct_used"] < 100]

    return {
        "month": month,
        "balance": balance,
        "monthly_summary": summary,
        "overdue_bills": overdue,
        "due_soon_bills": due_soon,
        "over_budget": over_budget,
        "near_budget": near_budget,
    }
