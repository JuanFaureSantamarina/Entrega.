#!/usr/bin/env python3
"""
Finanzas Personales — interfaz web (sin dependencias externas).

Uso:
  python webapp.py            # sirve en http://localhost:8000
  PORT=8080 python webapp.py  # puerto custom (para hosting)
"""

import html
import os
import sys
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from wsgiref.simple_server import make_server

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.db import init_db
from src.categories import list_categories
from src import transactions, bills, budgets, reports


# ─── HTML helpers ──────────────────────────────────────────────────────────────

STYLE = """
  :root { color-scheme: light dark; }
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, system-ui, sans-serif;
    max-width: 640px; margin: 0 auto; padding: 12px 16px 60px;
    background: #f4f5f7; color: #1a1a1a; line-height: 1.4;
  }
  @media (prefers-color-scheme: dark) {
    body { background: #16171a; color: #eee; }
    .card { background: #232428 !important; border-color: #333 !important; }
    input, select { background: #1b1c1f !important; color: #eee !important; border-color: #444 !important; }
  }
  h1 { font-size: 1.3rem; }
  h2 { font-size: 1.05rem; margin: 18px 0 8px; }
  nav {
    display: flex; gap: 6px; overflow-x: auto; margin-bottom: 14px;
    padding-bottom: 4px; -webkit-overflow-scrolling: touch;
  }
  nav a {
    flex: none; padding: 8px 12px; border-radius: 8px; background: #fff;
    border: 1px solid #ddd; text-decoration: none; color: #333; font-size: 0.9rem;
  }
  nav a.active { background: #2563eb; color: #fff; border-color: #2563eb; }
  .card {
    background: #fff; border: 1px solid #e3e3e3; border-radius: 10px;
    padding: 14px; margin-bottom: 12px;
  }
  .row { display: flex; justify-content: space-between; gap: 8px; padding: 6px 0; border-bottom: 1px solid #eee; }
  .row:last-child { border-bottom: none; }
  .row > *:first-child { min-width: 0; flex: 1 1 auto; overflow-wrap: break-word; }
  .row > *:last-child { flex: 0 0 auto; text-align: right; }
  .muted { color: #777; font-size: 0.85rem; }
  .green { color: #16a34a; } .red { color: #dc2626; } .yellow { color: #ca8a04; }
  .amount { font-weight: 600; white-space: nowrap; }
  form.inline { display: inline; }
  label { display: block; font-size: 0.85rem; margin: 10px 0 4px; color: #555; }
  input, select {
    width: 100%; padding: 10px; font-size: 1rem; border-radius: 8px;
    border: 1px solid #ccc; background: #fff;
  }
  button {
    margin-top: 14px; padding: 11px 16px; font-size: 1rem; border: none;
    border-radius: 8px; background: #2563eb; color: #fff; width: 100%;
  }
  button.secondary { background: #eee; color: #333; width: auto; margin: 0; }
  button.danger { background: #dc2626; width: auto; margin: 0; }
  .bar-bg { background: #e5e7eb; border-radius: 6px; height: 10px; overflow: hidden; margin-top: 4px; }
  .bar-fill { height: 100%; background: #2563eb; }
  .badge { font-size: 0.75rem; padding: 2px 8px; border-radius: 999px; font-weight: 600; }
  .badge.overdue { background: #fee2e2; color: #b91c1c; }
  .badge.due_soon { background: #fef3c7; color: #92400e; }
  .badge.upcoming { background: #e0f2fe; color: #0369a1; }
  .actions { display: flex; gap: 8px; margin-top: 6px; }
  .error { background: #fee2e2; color: #991b1b; padding: 10px; border-radius: 8px; margin-bottom: 12px; }
  .ok { background: #dcfce7; color: #166534; padding: 10px; border-radius: 8px; margin-bottom: 12px; }
"""

NAV_ITEMS = [
    ("/", "Dashboard"),
    ("/movimientos", "Movimientos"),
    ("/vencimientos", "Vencimientos"),
    ("/presupuestos", "Presupuestos"),
    ("/reportes", "Reportes"),
]


def money(n: float) -> str:
    return f"${n:,.2f}"


def e(s) -> str:
    return html.escape(str(s or ""), quote=True)


def page(path: str, title: str, body: str, msg: str = None, err: str = None) -> str:
    nav_html = "".join(
        f'<a href="{href}" class="{"active" if href == path else ""}">{label}</a>'
        for href, label in NAV_ITEMS
    )
    banner = ""
    if err:
        banner = f'<div class="error">{e(err)}</div>'
    elif msg:
        banner = f'<div class="ok">{e(msg)}</div>'
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} — Finanzas</title>
<style>{STYLE}</style>
</head>
<body>
<h1>💰 Finanzas Personales</h1>
<nav>{nav_html}</nav>
{banner}
{body}
</body>
</html>"""


def option_list(items, selected=None):
    return "".join(
        f'<option value="{e(i)}" {"selected" if i == selected else ""}>{e(i)}</option>'
        for i in items
    )


# ─── Pages ─────────────────────────────────────────────────────────────────────

def render_dashboard(qs):
    d = reports.dashboard()
    s = d["monthly_summary"]
    balance_class = "green" if d["balance"] >= 0 else "red"

    body = f"""
    <div class="card">
      <div class="muted">Balance total</div>
      <div class="amount {balance_class}" style="font-size:1.6rem">{money(d['balance'])}</div>
      <div class="row"><span class="muted">Ingresos ({d['month']})</span><span class="amount green">{money(s['income_total'])}</span></div>
      <div class="row"><span class="muted">Egresos ({d['month']})</span><span class="amount red">{money(s['expense_total'])}</span></div>
    </div>
    """

    if d["overdue_bills"]:
        rows = "".join(
            f'<div class="row"><span>❌ {e(b["name"])}<br><span class="muted">vencía {b["due_date"]}</span></span>'
            f'<span class="amount red">{money(b["amount"])}</span></div>'
            for b in d["overdue_bills"]
        )
        body += f'<div class="card"><h2>⚠ Vencimientos vencidos</h2>{rows}</div>'

    if d["due_soon_bills"]:
        rows = "".join(
            f'<div class="row"><span>⏰ {e(b["name"])}<br><span class="muted">vence {b["due_date"]}</span></span>'
            f'<span class="amount">{money(b["amount"])}</span></div>'
            for b in d["due_soon_bills"]
        )
        body += f'<div class="card"><h2>Próximos a vencer</h2>{rows}</div>'

    if not d["overdue_bills"] and not d["due_soon_bills"]:
        body += '<div class="card">✅ No hay vencimientos urgentes</div>'

    over = d["over_budget"] + d["near_budget"]
    if over:
        rows = "".join(
            f'<div class="row"><span>{e(b["category"])}</span>'
            f'<span class="{"red" if b["pct_used"] >= 100 else "yellow"}">{b["pct_used"]}%</span></div>'
            for b in over
        )
        body += f'<div class="card"><h2>Presupuestos a vigilar</h2>{rows}</div>'

    return page("/", "Dashboard", body)


def render_movimientos(qs):
    month = (qs.get("month") or [None])[0]
    movs = transactions.list_movements(month=month)

    income_opts = option_list(list_categories("income"))
    expense_opts = option_list(list_categories("expense"))
    today = date.today().isoformat()

    rows_html = ""
    for m in movs:
        color = "green" if m["type"] == "income" else "red"
        sign = "+" if m["type"] == "income" else "-"
        rows_html += f"""
        <div class="row">
          <span>{m['date']}<br><span class="muted">{e(m['category'])}{' · ' + e(m['description']) if m['description'] else ''}</span></span>
          <span>
            <span class="amount {color}">{sign}{money(m['amount'])}</span><br>
            <form class="inline" method="post" action="/movimientos/delete" onsubmit="return confirm('¿Eliminar este movimiento?')">
              <input type="hidden" name="id" value="{m['id']}">
              <button type="submit" class="secondary" style="padding:2px 8px;font-size:0.75rem;margin-top:4px">Eliminar</button>
            </form>
          </span>
        </div>"""

    if not rows_html:
        rows_html = '<p class="muted">No hay movimientos todavía.</p>'

    body = f"""
    <div class="card">
      <form method="get" action="/movimientos">
        <label>Filtrar por mes</label>
        <input type="month" name="month" value="{e(month or '')}" onchange="this.form.submit()">
      </form>
    </div>

    <div class="card">
      <h2>Ingreso</h2>
      <form method="post" action="/movimientos/add">
        <input type="hidden" name="type" value="income">
        <label>Monto</label>
        <input type="number" step="0.01" min="0.01" name="amount" required inputmode="decimal">
        <label>Categoría</label>
        <select name="category">{income_opts}</select>
        <label>Descripción (opcional)</label>
        <input type="text" name="desc">
        <label>Fecha</label>
        <input type="date" name="date" value="{today}">
        <button type="submit">Agregar ingreso</button>
      </form>
    </div>

    <div class="card">
      <h2>Egreso</h2>
      <form method="post" action="/movimientos/add">
        <input type="hidden" name="type" value="expense">
        <label>Monto</label>
        <input type="number" step="0.01" min="0.01" name="amount" required inputmode="decimal">
        <label>Categoría</label>
        <select name="category">{expense_opts}</select>
        <label>Descripción (opcional)</label>
        <input type="text" name="desc">
        <label>Fecha</label>
        <input type="date" name="date" value="{today}">
        <button type="submit">Agregar egreso</button>
      </form>
    </div>

    <div class="card">
      <h2>Movimientos {'de ' + month if month else ''}</h2>
      {rows_html}
    </div>
    """
    return page("/movimientos", "Movimientos", body)


def render_vencimientos(qs):
    status = (qs.get("status") or [None])[0]
    bs = bills.list_bills(status=status if status != "" else None)
    expense_opts = option_list(list_categories("expense"))
    today = date.today().isoformat()

    badge_labels = {"overdue": "VENCIDO", "due_soon": "PRÓXIMO", "upcoming": "a futuro", "paid": "pagado"}

    rows_html = ""
    for b in bs:
        cs = b["computed_status"]
        badge = f'<span class="badge {cs}">{badge_labels.get(cs, cs)}</span>'
        rows_html += f"""
        <div class="row" style="flex-direction:column;align-items:stretch">
          <div style="display:flex;justify-content:space-between">
            <span><strong>{e(b['name'])}</strong><br><span class="muted">{e(b['category'])} · vence {b['due_date']} · {b['recurring']}</span></span>
            <span class="amount">{money(b['amount'])}<br>{badge}</span>
          </div>
          <div class="actions">
            <form class="inline" method="post" action="/vencimientos/pagar">
              <input type="hidden" name="id" value="{b['id']}">
              <button type="submit" class="secondary">Pagar</button>
            </form>
            <form class="inline" method="post" action="/vencimientos/eliminar" onsubmit="return confirm('¿Eliminar este vencimiento?')">
              <input type="hidden" name="id" value="{b['id']}">
              <button type="submit" class="danger">Eliminar</button>
            </form>
          </div>
        </div>"""

    if not rows_html:
        rows_html = '<p class="muted">No hay vencimientos con ese filtro.</p>'

    body = f"""
    <div class="card">
      <form method="get" action="/vencimientos">
        <label>Filtrar por estado</label>
        <select name="status" onchange="this.form.submit()">
          <option value="" {"selected" if not status else ""}>Pendientes (default)</option>
          <option value="overdue" {"selected" if status == "overdue" else ""}>Vencidos</option>
          <option value="due_soon" {"selected" if status == "due_soon" else ""}>Próximos</option>
          <option value="all" {"selected" if status == "all" else ""}>Todos</option>
        </select>
      </form>
    </div>

    <div class="card">
      <h2>Nuevo vencimiento</h2>
      <form method="post" action="/vencimientos/add">
        <label>Nombre</label>
        <input type="text" name="name" required>
        <label>Monto</label>
        <input type="number" step="0.01" min="0.01" name="amount" required inputmode="decimal">
        <label>Categoría</label>
        <select name="category">{expense_opts}</select>
        <label>Fecha de vencimiento</label>
        <input type="date" name="due_date" value="{today}" required>
        <label>Recurrencia</label>
        <select name="recurring">
          <option value="none">Única vez</option>
          <option value="weekly">Semanal</option>
          <option value="monthly">Mensual</option>
          <option value="yearly">Anual</option>
        </select>
        <label>Notas (opcional)</label>
        <input type="text" name="notes">
        <button type="submit">Crear vencimiento</button>
      </form>
    </div>

    <div class="card">
      <h2>Vencimientos</h2>
      {rows_html}
    </div>
    """
    return page("/vencimientos", "Vencimientos", body)


def render_presupuestos(qs):
    month = (qs.get("month") or [None])[0] or date.today().strftime("%Y-%m")
    rows = budgets.budget_status(month)
    expense_opts = option_list(list_categories("expense"))

    rows_html = ""
    for r in rows:
        pct = min(r["pct_used"], 100)
        bar_color = "#dc2626" if r["pct_used"] >= 100 else ("#ca8a04" if r["pct_used"] >= 80 else "#2563eb")
        rows_html += f"""
        <div class="row" style="flex-direction:column;align-items:stretch">
          <div style="display:flex;justify-content:space-between">
            <span>{e(r['category'])}</span>
            <span class="amount">{money(r['spent'])} / {money(r['budget'])}</span>
          </div>
          <div class="bar-bg"><div class="bar-fill" style="width:{pct}%;background:{bar_color}"></div></div>
          <span class="muted">{r['pct_used']}% usado</span>
        </div>"""

    if not rows_html:
        rows_html = '<p class="muted">No hay presupuestos definidos para este mes.</p>'

    body = f"""
    <div class="card">
      <form method="get" action="/presupuestos">
        <label>Mes</label>
        <input type="month" name="month" value="{e(month)}" onchange="this.form.submit()">
      </form>
    </div>

    <div class="card">
      <h2>Definir presupuesto</h2>
      <form method="post" action="/presupuestos/set">
        <input type="hidden" name="month" value="{e(month)}">
        <label>Categoría</label>
        <select name="category">{expense_opts}</select>
        <label>Monto mensual</label>
        <input type="number" step="0.01" min="0.01" name="amount" required inputmode="decimal">
        <button type="submit">Guardar presupuesto</button>
      </form>
    </div>

    <div class="card">
      <h2>Estado de {month}</h2>
      {rows_html}
    </div>
    """
    return page("/presupuestos", "Presupuestos", body)


def render_reportes(qs):
    month = (qs.get("month") or [None])[0] or date.today().strftime("%Y-%m")
    s = reports.monthly_summary(month)
    balance_total = reports.overall_balance()

    max_amount = max(s["expense_by_category"].values()) if s["expense_by_category"] else 0
    cat_rows = ""
    for cat, amount in s["expense_by_category"].items():
        pct = (amount / max_amount * 100) if max_amount else 0
        cat_rows += f"""
        <div class="row" style="flex-direction:column;align-items:stretch">
          <div style="display:flex;justify-content:space-between">
            <span>{e(cat)}</span><span class="amount">{money(amount)}</span>
          </div>
          <div class="bar-bg"><div class="bar-fill" style="width:{pct}%"></div></div>
        </div>"""
    if not cat_rows:
        cat_rows = '<p class="muted">Sin egresos este mes.</p>'

    balance_class = "green" if s["balance"] >= 0 else "red"
    body = f"""
    <div class="card">
      <form method="get" action="/reportes">
        <label>Mes</label>
        <input type="month" name="month" value="{e(month)}" onchange="this.form.submit()">
      </form>
    </div>

    <div class="card">
      <h2>Resumen de {month}</h2>
      <div class="row"><span>Ingresos</span><span class="amount green">{money(s['income_total'])}</span></div>
      <div class="row"><span>Egresos</span><span class="amount red">{money(s['expense_total'])}</span></div>
      <div class="row"><span>Balance del mes</span><span class="amount {balance_class}">{money(s['balance'])}</span></div>
    </div>

    <div class="card">
      <div class="muted">Balance histórico total</div>
      <div class="amount {'green' if balance_total >= 0 else 'red'}" style="font-size:1.3rem">{money(balance_total)}</div>
    </div>

    <div class="card">
      <h2>Egresos por categoría</h2>
      {cat_rows}
    </div>
    """
    return page("/reportes", "Reportes", body)


# ─── WSGI app ──────────────────────────────────────────────────────────────────

def read_post(environ) -> dict:
    try:
        length = int(environ.get("CONTENT_LENGTH", 0) or 0)
    except ValueError:
        length = 0
    raw = environ["wsgi.input"].read(length) if length else b""
    return {k: v[0] for k, v in parse_qs(raw.decode("utf-8")).items()}


def redirect(start_response, location):
    start_response("303 See Other", [("Location", location)])
    return [b""]


def html_response(start_response, body: str, status="200 OK"):
    encoded = body.encode("utf-8")
    start_response(status, [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(encoded)))])
    return [encoded]


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    qs = parse_qs(environ.get("QUERY_STRING", ""))
    method = environ.get("REQUEST_METHOD", "GET")

    try:
        if method == "GET":
            if path == "/":
                return html_response(start_response, render_dashboard(qs))
            if path == "/movimientos":
                return html_response(start_response, render_movimientos(qs))
            if path == "/vencimientos":
                return html_response(start_response, render_vencimientos(qs))
            if path == "/presupuestos":
                return html_response(start_response, render_presupuestos(qs))
            if path == "/reportes":
                return html_response(start_response, render_reportes(qs))
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"404 Not Found"]

        if method == "POST":
            form = read_post(environ)

            if path == "/movimientos/add":
                try:
                    transactions.add_movement(
                        form.get("type"), float(form.get("amount", 0)),
                        form.get("category"), form.get("desc", ""), form.get("date") or None,
                    )
                except (ValueError, TypeError):
                    pass
                return redirect(start_response, "/movimientos")

            if path == "/movimientos/delete":
                try:
                    transactions.delete_movement(int(form.get("id")))
                except (ValueError, TypeError):
                    pass
                return redirect(start_response, "/movimientos")

            if path == "/vencimientos/add":
                try:
                    bills.add_bill(
                        form.get("name"), float(form.get("amount", 0)), form.get("category"),
                        form.get("due_date"), form.get("recurring", "none"), form.get("notes", ""),
                    )
                except (ValueError, TypeError):
                    pass
                return redirect(start_response, "/vencimientos")

            if path == "/vencimientos/pagar":
                try:
                    bills.pay_bill(int(form.get("id")))
                except (ValueError, TypeError):
                    pass
                return redirect(start_response, "/vencimientos")

            if path == "/vencimientos/eliminar":
                try:
                    bills.delete_bill(int(form.get("id")))
                except (ValueError, TypeError):
                    pass
                return redirect(start_response, "/vencimientos")

            if path == "/presupuestos/set":
                try:
                    budgets.set_budget(form.get("category"), float(form.get("amount", 0)), form.get("month") or None)
                except (ValueError, TypeError):
                    pass
                return redirect(start_response, f"/presupuestos?month={form.get('month', '')}")

            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"404 Not Found"]

    except Exception as exc:
        body = page(path, "Error", f'<div class="card">Ocurrió un error: {e(exc)}</div>')
        return html_response(start_response, body, status="500 Internal Server Error")

    start_response("405 Method Not Allowed", [("Content-Type", "text/plain")])
    return [b"405 Method Not Allowed"]


def main():
    init_db()
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    with make_server(host, port, application) as httpd:
        print(f"Finanzas Personales corriendo en http://{host}:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
