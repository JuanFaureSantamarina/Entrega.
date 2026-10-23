# Job Application Automation

Automatizá tus postulaciones laborales con IA. La app tailoriza tu CV, genera cartas de presentación y registra todas tus postulaciones, organizado por nichos.

## Características

- **CV inteligente**: Claude AI adapta tu CV base para cada oferta laboral
- **Cartas de presentación**: Generación automática personalizada al puesto
- **Nichos**: Tech, Marketing, Finanzas, Data Science, RRHH (fácilmente extensibles)
- **PDFs profesionales**: Documentos listos para enviar
- **Envío por email**: Automatización del envío con attachments
- **Tracking**: Base de datos SQLite para seguimiento de todas tus postulaciones

## Setup

### 1. Instalá dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurá credenciales

```bash
cp .env.example .env
# Editá .env con tu API key de Anthropic y credenciales de email
```

Para obtener una API key de Anthropic: https://console.anthropic.com

Para Gmail, necesitás una **App Password** (no tu contraseña normal):
1. Activá 2FA en tu cuenta de Google
2. Ve a Cuenta de Google → Seguridad → Contraseñas de aplicación
3. Generá una para "Correo"

### 3. Completá tu CV base

```bash
# Editá data/base_cv.yaml con toda tu información profesional
```

### 4. Verificá la configuración

```bash
python main.py init
```

## Uso

### Postularse a un trabajo

```bash
# Interactivo (te pide la descripción del puesto)
python main.py apply -c "Empresa XYZ" -p "Desarrollador Python"

# Con carta de presentación y envío automático
python main.py apply -c "Empresa XYZ" -p "Desarrollador Python" \
  --cover-letter \
  --email rrhh@empresa.com \
  --send-email

# Desde archivo con descripción del puesto
python main.py apply -c "Empresa XYZ" -p "Desarrollador Python" \
  -f descripcion.txt \
  --niche tech \
  --cover-letter
```

### Gestionar nichos

```bash
python main.py niches list          # Ver todos los nichos
python main.py niches show tech     # Ver detalles de un nicho
```

### Seguimiento de postulaciones

```bash
python main.py track list                         # Ver todas las postulaciones
python main.py track list --niche tech            # Filtrar por nicho
python main.py track list --status entrevista     # Filtrar por estado
python main.py track update 3 --status entrevista # Actualizar estado
python main.py track stats                        # Ver estadísticas
```

### Generar CVs

```bash
python main.py cv preview              # Generar preview del CV base
python main.py cv generate -c "Empresa" -p "Puesto" -n tech -f descripcion.txt
```

## Búsqueda automática de ofertas

El buscador revisa cada mañana (lunes a viernes, 07:17 hora Argentina) estas fuentes y guarda las ofertas que encajan con el perfil en `data/jobs/ofertas.json`:

- **LinkedIn** (búsqueda pública): Argentina, solo remoto e híbrido, publicadas en las últimas 24 h.
- **Remotive y Himalayas**: trabajos remotos de empresas de afuera abiertos a LATAM / Argentina.
- **Portales de empresas grandes** (Workday, Greenhouse, Lever): Givaudan, Mondelez, Coca-Cola, J&J, Pfizer, Salesforce, Mastercard, Nubank, dLocal…

Cada oferta recibe un puntaje de 0 a 100 según el título, las skills del CV, si es una empresa objetivo, la modalidad y la seniority. Las presenciales y las de otros rubros (desarrollo, ventas, etc.) se descartan.

```bash
python main.py jobs search            # buscar ahora
python main.py jobs search --dry-run  # probar sin guardar
python main.py jobs list --min 50     # ver las mejores de la última semana
```

Todo se ajusta en `config/search.yaml`: palabras clave, empresas objetivo, títulos a excluir, puntaje mínimo y fuentes. Si una fuente falla, las demás siguen y el error queda en `data/jobs/estado.json`.

El workflow está en `.github/workflows/buscar-ofertas.yml`. GitHub solo ejecuta los workflows programados que están en la rama principal del repo, y también se puede lanzar a mano desde la pestaña **Actions** → **Buscar ofertas** → **Run workflow**.

### Radar Laboral (tracker)

Las ofertas se siguen en el tracker publicado como artifact en claude.ai (base de datos propia): estado de cada oferta (nueva → para postular → postulado → entrevista → oferta), notas y filtros Argentina / Afuera. Una tarea programada de Claude lee `data/jobs/ofertas.json`, revisa las mejores contra el CV y las carga en el tracker.

## Nichos disponibles

| ID | Nombre | Descripción |
|----|--------|-------------|
| `tech` | Tecnología | Software, DevOps, QA, infraestructura |
| `marketing` | Marketing y Comunicación | Digital, contenido, branding, PR |
| `finance` | Finanzas y Contabilidad | Corporate finance, auditoría, controlling |
| `data_science` | Data Science e IA | ML, analytics, BI, estadística |
| `hr` | Recursos Humanos | Selección, capacitación, cultura |
| `operaciones` | Operaciones y Procesos | Análisis de procesos, mejora continua, business operations |
| `administracion` | Administración y Finanzas | Cobranzas, pagos, costos, compras, control de gestión |

### Agregar un nicho personalizado

Creá un archivo `config/niches/mi_nicho.yaml`:

```yaml
name: "Nombre del nicho"
description: "Descripción breve"
keywords:
  - palabra_clave_1
  - palabra_clave_2
skills_to_highlight:
  - "Habilidad relevante para este nicho"
tone: "profesional y dinámico"
emphasis: "logros cuantificables y proyectos"
```

## Estados de postulación

- `enviada` - Aplicación enviada
- `en_proceso` - En proceso de selección
- `entrevista` - Entrevista agendada
- `oferta` - Oferta recibida
- `rechazada` - No avanzó
- `descartada` - Descartada por el candidato

## Estructura del proyecto

```
.
├── main.py                    # CLI principal
├── config/
│   ├── settings.yaml          # Configuración de la app
│   └── niches/                # Configuración por nicho
│       ├── tech.yaml
│       ├── marketing.yaml
│       ├── finance.yaml
│       ├── data_science.yaml
│       └── hr.yaml
├── data/
│   ├── base_cv.yaml           # Tu CV base (completalo!)
│   └── applications.db        # Base de datos de postulaciones (auto-creada)
├── src/
│   ├── ai_engine.py           # Integración con Claude API
│   ├── cv_generator.py        # Generación de PDFs de CV
│   ├── cover_letter_generator.py  # Generación de cartas en PDF
│   ├── email_sender.py        # Envío de emails
│   ├── niche_manager.py       # Gestión de nichos
│   └── tracker.py             # Seguimiento de postulaciones
├── output/
│   ├── cvs/                   # CVs generados
│   └── cover_letters/         # Cartas generadas
├── requirements.txt
└── .env.example
```
