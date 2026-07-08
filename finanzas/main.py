#!/usr/bin/env python3
"""
Finanzas Personales — CLI para ordenar ingresos, egresos, vencimientos y presupuestos.

Uso rápido:
  python main.py init
  python main.py mov add --type income -a 500000 -c Sueldo
  python main.py mov add --type expense -a 30000 -c Comida --desc "Super"
  python main.py bill add --name Alquiler -a 200000 -c Vivienda --due-date 2026-07-10 --recurring monthly
  python main.py bill pay 1
  python main.py budget set -c Comida -a 100000
  python main.py report month
  python main.py dashboard
"""

import argparse
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
CYAN   = "\033[36m"
RED    = "\033[31m"
DIM    = "\033[2m"


def c(color: str, text: str) -> str:
    return f"{color}{text}{RESET}"

def ok(msg):   print(c(GREEN,  f"✓ {msg}"))
def warn(msg): print(c(YELLOW, f"! {msg}"))
def err(msg):  print(c(RED,    f"✗ {msg}"), file=sys.stderr)
def info(msg): print(c(DIM,    f"  {msg}"))
def head(msg): print(f"\n{c(BOLD+BLUE, msg)}")


def money(n: float) -> str:
    return f"${n:,.2f}"


# ─── Command: init ────────────────────────────────────────────────────────────

def cmd_init(args):
    head("Inicializando Finanzas Personales...")
    from src.db import init_db, DB_PATH
    init_db()
    ok(f"Base de datos lista en {DB_PATH}")

    from src.categories import load_categories
    cats = load_categories()
    ok(f"{len(cats['income'])} categorías de ingreso, {len(cats['expense'])} de egreso")

    print()
    print(c(BOLD+CYAN, "Flujo recomendado:"))
    print("  1. python main.py mov add --type income -a 500000 -c Sueldo")
    print("  2. python main.py bill add --name Alquiler -a 200000 -c Vivienda --due-date 2026-07-10 --recurring monthly")
    print("  3. python main.py budget set -c Comida -a 100000")
    print("  4. python main.py dashboard")


# ─── Command: categories ──────────────────────────────────────────────────────

def cmd_categories_list(args):
    from src.categories import load_categories
    cats = load_categories()
    head("Categorías de ingreso")
    for cat in cats["income"]:
        print(f"  {c(GREEN,'•')} {cat}")
    head("Categorías de egreso")
    for cat in cats["expense"]:
        print(f"  {c(RED,'•')} {cat}")


# ─── Command: mov (movements) ─────────────────────────────────────────────────

def cmd_mov_add(args):
    from src.transactions import add_movement
    try:
        mid = add_movement(args.type, args.amount, args.category, args.desc or "", args.date)
    except ValueError as e:
        err(str(e)); sys.exit(1)
    label = "Ingreso" if args.type == "income" else "Egreso"
    color = GREEN if args.type == "income" else RED
    ok(f"{c(color, label)} registrado (ID: {mid}) — {money(args.amount)} en {args.category}")


def cmd_mov_list(args):
    from src.transactions import list_movements
    movs = list_movements(month=args.month, type_=args.type, category=args.category)
    if not movs:
        warn("No hay movimientos con esos filtros.")
        return

    head(f"Movimientos ({len(movs)} total)")
    fmt = "  {:<4} {:<10} {:<10} {:<22} {:<28} {}"
    print(c(DIM, fmt.format("ID", "Fecha", "Tipo", "Categoría", "Descripción", "Monto")))
    print(c(DIM, "  " + "-" * 92))
    for m in movs:
        color = GREEN if m["type"] == "income" else RED
        sign = "+" if m["type"] == "income" else "-"
        print(fmt.format(
            str(m["id"]),
            m["date"][:10],
            c(color, "ingreso" if m["type"] == "income" else "egreso"),
            m["category"][:22],
            (m["description"] or "")[:28],
            c(color, f"{sign}{money(m['amount'])}"),
        ))


def cmd_mov_delete(args):
    from src.transactions import delete_movement
    if delete_movement(args.id):
        ok(f"Movimiento {args.id} eliminado")
    else:
        err(f"No existe el movimiento {args.id}")
        sys.exit(1)


# ─── Command: bill (vencimientos) ─────────────────────────────────────────────

STATUS_LABELS = {
    "overdue":   (RED,    "VENCIDO"),
    "due_soon":  (YELLOW, "PRÓXIMO"),
    "upcoming":  (CYAN,   "próximo"),
    "paid":      (DIM,    "pagado"),
}


def cmd_bill_add(args):
    from src.bills import add_bill
    try:
        bid = add_bill(args.name, args.amount, args.category, args.due_date, args.recurring, args.notes or "")
    except ValueError as e:
        err(str(e)); sys.exit(1)
    ok(f"Vencimiento creado (ID: {bid}) — {args.name}: {money(args.amount)}, vence {args.due_date}")


def cmd_bill_list(args):
    from src.bills import list_bills
    bills = list_bills(status=args.status, soon_days=args.soon_days)
    if not bills:
        warn("No hay vencimientos con esos filtros.")
        return

    head(f"Vencimientos ({len(bills)} total)")
    fmt = "  {:<4} {:<20} {:<18} {:<12} {:<10} {:<10} {}"
    print(c(DIM, fmt.format("ID", "Nombre", "Categoría", "Vence", "Monto", "Recurr.", "Estado")))
    print(c(DIM, "  " + "-" * 92))
    for b in bills:
        color, label = STATUS_LABELS.get(b["computed_status"], ("", b["computed_status"]))
        print(fmt.format(
            str(b["id"]),
            b["name"][:20],
            b["category"][:18],
            b["due_date"],
            money(b["amount"]),
            b["recurring"],
            c(color, label),
        ))


def cmd_bill_pay(args):
    from src.bills import pay_bill
    try:
        bill = pay_bill(args.id, args.date)
    except ValueError as e:
        err(str(e)); sys.exit(1)
    ok(f"Vencimiento {args.id} ('{bill['name']}') pagado — registrado como egreso")
    if bill["recurring"] != "none":
        info(f"Próximo vencimiento: {bill['due_date']}")


def cmd_bill_delete(args):
    from src.bills import delete_bill
    if delete_bill(args.id):
        ok(f"Vencimiento {args.id} eliminado")
    else:
        err(f"No existe el vencimiento {args.id}")
        sys.exit(1)


# ─── Command: budget ──────────────────────────────────────────────────────────

def cmd_budget_set(args):
    from src.budgets import set_budget
    try:
        set_budget(args.category, args.amount, args.month)
    except ValueError as e:
        err(str(e)); sys.exit(1)
    month = args.month or date.today().strftime("%Y-%m")
    ok(f"Presupuesto de {args.category} para {month}: {money(args.amount)}")


def cmd_budget_status(args):
    from src.budgets import budget_status
    month = args.month or date.today().strftime("%Y-%m")
    rows = budget_status(args.month)
    if not rows:
        warn(f"No hay presupuestos configurados para {month}.")
        return

    head(f"Presupuestos de {month}")
    fmt = "  {:<22} {:<12} {:<12} {:<12} {}"
    print(c(DIM, fmt.format("Categoría", "Presup.", "Gastado", "Resta", "% usado")))
    print(c(DIM, "  " + "-" * 76))
    for r in rows:
        pct = r["pct_used"]
        color = RED if pct >= 100 else (YELLOW if pct >= 80 else GREEN)
        bar = "█" * min(int(pct / 5), 20)
        print(fmt.format(
            r["category"][:22],
            money(r["budget"]),
            money(r["spent"]),
            money(r["remaining"]),
            c(color, f"{pct}% {bar}"),
        ))


# ─── Command: report ──────────────────────────────────────────────────────────

def cmd_report_month(args):
    from src.reports import monthly_summary
    s = monthly_summary(args.month)
    head(f"Resumen de {s['month']}")
    print(f"  {c(GREEN, 'Ingresos:')}  {money(s['income_total'])}")
    print(f"  {c(RED,   'Egresos:')}   {money(s['expense_total'])}")
    balance_color = GREEN if s["balance"] >= 0 else RED
    print(f"  {c(BOLD, 'Balance:')}   {c(balance_color, money(s['balance']))}")

    if s["expense_by_category"]:
        print(f"\n  {c(BOLD, 'Egresos por categoría:')}")
        max_amount = max(s["expense_by_category"].values())
        for cat, amount in s["expense_by_category"].items():
            bar_len = int((amount / max_amount) * 30) if max_amount else 0
            print(f"    {cat:<24} {money(amount):>14}  {c(CYAN, '█' * bar_len)}")


def cmd_report_balance(args):
    from src.reports import overall_balance
    balance = overall_balance()
    color = GREEN if balance >= 0 else RED
    head("Balance histórico")
    print(f"  {c(BOLD, 'Balance total:')} {c(color, money(balance))}")


# ─── Command: dashboard ───────────────────────────────────────────────────────

def cmd_dashboard(args):
    from src.reports import dashboard
    d = dashboard(soon_days=args.soon_days)

    head(f"Dashboard — {d['month']}")
    balance_color = GREEN if d["balance"] >= 0 else RED
    print(f"  {c(BOLD, 'Balance total:')} {c(balance_color, money(d['balance']))}")

    s = d["monthly_summary"]
    print(f"  {c(GREEN, 'Ingresos del mes:')} {money(s['income_total'])}   "
          f"{c(RED, 'Egresos del mes:')} {money(s['expense_total'])}")

    if d["overdue_bills"]:
        head(f"⚠ Vencimientos VENCIDOS ({len(d['overdue_bills'])})")
        for b in d["overdue_bills"]:
            print(f"  {c(RED, '✗')} {b['name']:<24} {money(b['amount']):>14}  vencía {b['due_date']}")

    if d["due_soon_bills"]:
        head(f"⏰ Próximos a vencer ({len(d['due_soon_bills'])})")
        for b in d["due_soon_bills"]:
            print(f"  {c(YELLOW, '•')} {b['name']:<24} {money(b['amount']):>14}  vence {b['due_date']}")

    if not d["overdue_bills"] and not d["due_soon_bills"]:
        ok("No hay vencimientos urgentes")

    if d["over_budget"]:
        head(f"🚨 Presupuestos excedidos ({len(d['over_budget'])})")
        for b in d["over_budget"]:
            print(f"  {c(RED, '✗')} {b['category']:<24} {b['pct_used']}% usado ({money(b['spent'])} / {money(b['budget'])})")

    if d["near_budget"]:
        head(f"⚠ Presupuestos cerca del límite ({len(d['near_budget'])})")
        for b in d["near_budget"]:
            print(f"  {c(YELLOW, '•')} {b['category']:<24} {b['pct_used']}% usado ({money(b['spent'])} / {money(b['budget'])})")


# ─── Parser ───────────────────────────────────────────────────────────────────

def valid_date(s: str) -> str:
    datetime.strptime(s, "%Y-%m-%d")
    return s


def valid_month(s: str) -> str:
    datetime.strptime(s, "%Y-%m")
    return s


def build_parser():
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Finanzas Personales — Ordená tus ingresos, egresos y vencimientos",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Inicializar la base de datos")
    sub.add_parser("dashboard", help="Ver resumen general y alertas").add_argument(
        "--soon-days", type=int, default=7, help="Días para considerar un vencimiento 'próximo' (default: 7)"
    )

    # categories
    p_cat = sub.add_parser("categories", help="Ver categorías disponibles")
    cat_sub = p_cat.add_subparsers(dest="cat_cmd", required=True)
    cat_sub.add_parser("list", help="Listar categorías")

    # mov
    p_mov = sub.add_parser("mov", help="Gestión de movimientos (ingresos/egresos)")
    mov_sub = p_mov.add_subparsers(dest="mov_cmd", required=True)

    p_mov_add = mov_sub.add_parser("add", help="Registrar un movimiento")
    p_mov_add.add_argument("--type", "-t", choices=["income", "expense"], required=True)
    p_mov_add.add_argument("--amount", "-a", type=float, required=True)
    p_mov_add.add_argument("--category", "-c", required=True)
    p_mov_add.add_argument("--desc", help="Descripción opcional")
    p_mov_add.add_argument("--date", "-d", type=valid_date, help="YYYY-MM-DD (default: hoy)")

    p_mov_list = mov_sub.add_parser("list", help="Listar movimientos")
    p_mov_list.add_argument("--month", "-m", type=valid_month, help="YYYY-MM")
    p_mov_list.add_argument("--type", "-t", choices=["income", "expense"])
    p_mov_list.add_argument("--category", "-c")

    p_mov_del = mov_sub.add_parser("delete", help="Eliminar un movimiento")
    p_mov_del.add_argument("id", type=int)

    # bill
    p_bill = sub.add_parser("bill", help="Gestión de vencimientos")
    bill_sub = p_bill.add_subparsers(dest="bill_cmd", required=True)

    p_bill_add = bill_sub.add_parser("add", help="Crear un vencimiento")
    p_bill_add.add_argument("--name", required=True)
    p_bill_add.add_argument("--amount", "-a", type=float, required=True)
    p_bill_add.add_argument("--category", "-c", required=True)
    p_bill_add.add_argument("--due-date", type=valid_date, required=True, help="YYYY-MM-DD")
    p_bill_add.add_argument("--recurring", choices=["none", "weekly", "monthly", "yearly"], default="none")
    p_bill_add.add_argument("--notes")

    p_bill_list = bill_sub.add_parser("list", help="Listar vencimientos")
    p_bill_list.add_argument("--status", "-s", choices=["pending", "paid", "overdue", "due_soon", "upcoming", "all"])
    p_bill_list.add_argument("--soon-days", type=int, default=7)

    p_bill_pay = bill_sub.add_parser("pay", help="Marcar un vencimiento como pagado")
    p_bill_pay.add_argument("id", type=int)
    p_bill_pay.add_argument("--date", "-d", type=valid_date, help="YYYY-MM-DD (default: hoy)")

    p_bill_del = bill_sub.add_parser("delete", help="Eliminar un vencimiento")
    p_bill_del.add_argument("id", type=int)

    # budget
    p_budget = sub.add_parser("budget", help="Gestión de presupuestos por categoría")
    budget_sub = p_budget.add_subparsers(dest="budget_cmd", required=True)

    p_budget_set = budget_sub.add_parser("set", help="Definir presupuesto de una categoría")
    p_budget_set.add_argument("--category", "-c", required=True)
    p_budget_set.add_argument("--amount", "-a", type=float, required=True)
    p_budget_set.add_argument("--month", "-m", type=valid_month, help="YYYY-MM (default: mes actual)")

    p_budget_status = budget_sub.add_parser("status", help="Ver estado de presupuestos")
    p_budget_status.add_argument("--month", "-m", type=valid_month, help="YYYY-MM (default: mes actual)")

    # report
    p_report = sub.add_parser("report", help="Reportes")
    report_sub = p_report.add_subparsers(dest="report_cmd", required=True)

    p_report_month = report_sub.add_parser("month", help="Resumen mensual")
    p_report_month.add_argument("--month", "-m", type=valid_month, help="YYYY-MM (default: mes actual)")

    report_sub.add_parser("balance", help="Balance histórico total")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    sub_cmd = (
        getattr(args, "cat_cmd", None)
        or getattr(args, "mov_cmd", None)
        or getattr(args, "bill_cmd", None)
        or getattr(args, "budget_cmd", None)
        or getattr(args, "report_cmd", None)
    )

    dispatch = {
        ("init",       None):     cmd_init,
        ("dashboard",  None):     cmd_dashboard,
        ("categories", "list"):   cmd_categories_list,
        ("mov",        "add"):    cmd_mov_add,
        ("mov",        "list"):   cmd_mov_list,
        ("mov",        "delete"): cmd_mov_delete,
        ("bill",       "add"):    cmd_bill_add,
        ("bill",       "list"):   cmd_bill_list,
        ("bill",       "pay"):    cmd_bill_pay,
        ("bill",       "delete"): cmd_bill_delete,
        ("budget",     "set"):    cmd_budget_set,
        ("budget",     "status"): cmd_budget_status,
        ("report",     "month"):  cmd_report_month,
        ("report",     "balance"): cmd_report_balance,
    }

    fn = dispatch.get((args.command, sub_cmd))
    if fn:
        fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
