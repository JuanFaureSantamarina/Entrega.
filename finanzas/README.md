# Finanzas Personales

App para ordenarte financieramente: registrá ingresos y egresos, llevá un
control de vencimientos (facturas, alquiler, tarjetas), definí presupuestos
por categoría y mirá un dashboard con alertas.

Tiene dos interfaces que comparten la misma base de datos:

- **`main.py`** — línea de comandos (CLI)
- **`webapp.py`** — interfaz web (para usar desde el navegador, ideal celular). No usa ninguna dependencia externa (solo librería estándar de Python), así que se puede hostear gratis en cualquier lado sin instalar nada más que Python.

> Esta app es independiente del resto del repositorio (no comparte código,
> dependencias ni base de datos con otros proyectos).

## Características

- **Movimientos**: registro de ingresos y egresos por categoría, con fecha y descripción
- **Vencimientos**: facturas y pagos recurrentes (semanal/mensual/anual) con alertas de vencidos y próximos a vencer
- **Pago de vencimientos**: al pagar un vencimiento se registra automáticamente como egreso, y si es recurrente se calcula la próxima fecha
- **Presupuestos**: límite de gasto mensual por categoría, con % de uso
- **Reportes**: resumen mensual (ingresos vs egresos, balance, gasto por categoría) y balance histórico
- **Dashboard**: vista rápida con balance, vencimientos urgentes y presupuestos excedidos

## Setup

```bash
cd finanzas
pip install -r requirements.txt
python main.py init
```

## Interfaz web (recomendada para celular / iPhone)

```bash
python webapp.py
```

Esto levanta un servidor en `http://localhost:8000` — abrí esa dirección en
el navegador. Es responsive (se adapta bien a pantallas de celular).

### Publicarla gratis para usarla desde el iPhone

Como no tiene dependencias externas, se puede hostear gratis en cualquier
servicio que corra Python, por ejemplo **[Render](https://render.com)** (plan free):

1. Subí este repo a GitHub (público o privado, Render soporta ambos con login).
2. En Render: `New` → `Web Service` → conectá el repo.
3. **Root Directory**: `finanzas`
4. **Build Command**: (dejar vacío, no hay dependencias que instalar)
5. **Start Command**: `python webapp.py`
6. Render define la variable `PORT` automáticamente — `webapp.py` ya la lee sola.
7. Deploy. Te da una URL pública (`https://tu-app.onrender.com`) — esa la abrís desde Safari en el iPhone, la agregás a la pantalla de inicio (Compartir → "Agregar a inicio") y queda como un ícono más, sin instalar nada.

**Importante:** en el plan free de Render la app se "duerme" tras un rato sin uso
(tarda ~30 seg en volver a arrancar la primera vez que la abrís) y el disco
no es persistente entre reinicios de la app, así que la base SQLite podría
resetearse en algún redeploy. Para uso personal está bien; si querés que los
datos nunca se pierdan, contame y vemos un disco persistente (también gratis
hasta cierto tamaño) o pasar a una base de datos externa.

## Uso (línea de comandos)

### Movimientos (ingresos/egresos)

```bash
python main.py mov add --type income -a 500000 -c Sueldo --desc "Sueldo julio"
python main.py mov add --type expense -a 30000 -c Comida --desc "Supermercado"

python main.py mov list                      # todos
python main.py mov list --month 2026-07      # filtrar por mes
python main.py mov list --type expense -c Comida

python main.py mov delete 3
```

### Vencimientos

```bash
# Único
python main.py bill add --name "Service auto" -a 45000 -c Transporte --due-date 2026-07-15

# Recurrente (mensual)
python main.py bill add --name Alquiler -a 200000 -c "Vivienda (alquiler/expensas)" \
  --due-date 2026-07-10 --recurring monthly

python main.py bill list                    # pendientes (vencidos + próximos + a futuro)
python main.py bill list --status overdue   # solo vencidos
python main.py bill list --status all       # incluye pagados

python main.py bill pay 1                   # marca como pagado (registra el egreso)
python main.py bill delete 2
```

### Presupuestos

```bash
python main.py budget set -c Comida -a 100000
python main.py budget set -c Comida -a 100000 --month 2026-08

python main.py budget status                # mes actual
python main.py budget status --month 2026-07
```

### Reportes y dashboard

```bash
python main.py report month                 # resumen del mes actual
python main.py report month --month 2026-06
python main.py report balance               # balance histórico total

python main.py dashboard                    # resumen + alertas de vencimientos y presupuestos
```

### Categorías

```bash
python main.py categories list
```

Las categorías por defecto están en `config/categories.yaml` — se pueden
editar o agregar nuevas directamente en ese archivo.

## Estructura del proyecto

```
finanzas/
├── main.py                  # CLI principal
├── webapp.py                # Interfaz web (sin dependencias externas)
├── config/
│   └── categories.yaml      # Categorías de ingreso/egreso
├── data/
│   └── finanzas.db          # Base de datos SQLite (auto-creada)
├── src/
│   ├── db.py                # Conexión y esquema de la base de datos
│   ├── categories.py        # Carga de categorías
│   ├── transactions.py      # Ingresos y egresos
│   ├── bills.py             # Vencimientos y su lógica de recurrencia
│   ├── budgets.py           # Presupuestos por categoría/mes
│   └── reports.py           # Resúmenes y dashboard
├── requirements.txt
└── .gitignore
```
