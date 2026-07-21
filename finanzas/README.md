# Finanzas Personales

App para ordenarte financieramente: registrá ingresos y egresos, llevá un
control de vencimientos (facturas, alquiler, tarjetas), definí presupuestos
por categoría y mirá un dashboard con alertas.

Tiene dos interfaces que comparten la misma base de datos:

- **`main.py`** — línea de comandos (CLI)
- **`webapp.py`** — interfaz web (para usar desde el navegador, ideal celular). Solo depende de PyYAML (en `requirements.txt`), todo lo demás es librería estándar de Python.

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

El repo incluye un `render.yaml` (Render Blueprint) con todo pre-configurado
— rootDir, build command, start command y el puerto. Publicarla es un click:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/JuanFaureSantamarina/Entrega./tree/claude/personal-finance-app-3gk1h6)

1. Click en el botón de arriba (o entrá a ese link).
2. Iniciá sesión / creá cuenta en Render con tu GitHub (esto lo tenés que hacer vos — ningún tercero puede loguearse en tu nombre).
3. Render va a mostrar el plan detectado desde `render.yaml` (servicio `finanzas-personales`, plan Free). Click en **Apply**.
4. Esperá ~1-2 minutos al primer deploy. Te va a quedar una URL pública tipo `https://finanzas-personales.onrender.com`.
5. Abrí esa URL en Safari en el iPhone → botón Compartir → **"Agregar a inicio"**. Te queda como un ícono más, sin instalar nada de la App Store.

Si preferís hacerlo a mano (sin el botón): `New` → `Web Service` → conectás el
repo → Root Directory `finanzas` → Build Command `pip install -r requirements.txt`
→ Start Command `python webapp.py`.

**Importante:** en el plan free de Render el disco no es persistente entre
redeploys/reinicios, así que la base SQLite local podría resetearse. Para que
los datos nunca se pierdan, seguí la sección de abajo (base de datos
persistente gratis).

### Que los datos nunca se pierdan (base de datos persistente gratis)

La app soporta guardar en **[Turso](https://turso.tech)** (base de datos SQLite
remota, gratis) en vez del disco local de Render. Es opt-in: si no configurás
nada, sigue usando el archivo local igual que antes.

1. Creá una cuenta gratis en [turso.tech](https://turso.tech) (podés entrar con GitHub).
2. Creá una base de datos nueva (botón "Create Database" en el dashboard).
3. Copiá la **URL de conexión** (empieza con `libsql://...`).
4. Generá un **token de acceso** para esa base (en la sección de la base, algo como "Create Token" / "Generate Token") y copialo.
5. En Render, andá al servicio `finanzas-personales` → **Settings** → **Environment** → agregá dos variables:
   - `TURSO_DATABASE_URL` → la URL del paso 3
   - `TURSO_AUTH_TOKEN` → el token del paso 4
6. Guardá — Render redeploya solo con las variables nuevas. A partir de ahí, todo lo que cargues en la web queda guardado en Turso y sobrevive a cualquier redeploy o reinicio.

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
