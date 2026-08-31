# MOTURI — Meditaciones

Biblioteca de meditaciones de MOTURI: una experiencia web independiente
(no forma parte de la app principal) pensada para abrirse desde un link
directo o un código QR, por ejemplo desde el journal físico de MOTURI.

Organiza meditaciones alojadas en YouTube por categoría y nivel, permite
reproducirlas embebidas dentro de la web, e incluye un "Desafío de 10 días"
con progreso guardado en el dispositivo (sin cuentas, sin login).

## Stack

- [Next.js 14](https://nextjs.org/) (App Router) + React 18
- [Tailwind CSS](https://tailwindcss.com/) para estilos
- JavaScript plano (sin TypeScript), para que el contenido sea fácil de
  editar sin conocimientos técnicos avanzados
- Sin backend, sin base de datos: todo el contenido vive en archivos de
  datos dentro del proyecto; el progreso del desafío se guarda en
  `localStorage` del navegador

## 1. Instalar dependencias

Necesitás [Node.js](https://nodejs.org/) 18 o superior.

```bash
cd moturi-meditaciones
npm install
```

## 2. Ejecutar localmente

```bash
npm run dev
```

Abrí [http://localhost:3000](http://localhost:3000). Los cambios en el
código se reflejan al instante.

Para probar el build de producción localmente:

```bash
npm run build
npm run start
```

## 3. Cambiar el logo

Todavía no hay un archivo de logo oficial en el proyecto: mientras tanto se
muestra el texto "MOTURI" estilizado.

Para poner el logo real:

1. Colocá el archivo en `public/logo.svg` (preferido) o `public/logo.png`.
2. Editá `src/components/Logo.jsx` y reemplazá el `<span>MOTURI</span>` por
   una imagen, por ejemplo:

   ```jsx
   <img src="/logo.svg" alt="MOTURI" className={className} />
   ```

Ese es el único archivo que hay que tocar: el logo se usa automáticamente
en la barra de navegación y en la portada.

## 4. Agregar o reemplazar links de YouTube

Todas las meditaciones están en **`src/data/meditations.js`**, con un
placeholder único por video en el campo `youtubeUrl`, por ejemplo:

```js
youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_CALMA_NIVEL_1",
```

Para activar un video real:

1. Buscá el placeholder correspondiente en `src/data/meditations.js`
   (cada uno es único e identificable: categoría + nivel).
2. Reemplazalo por la URL real de YouTube, por ejemplo:
   `https://www.youtube.com/watch?v=XXXXXXXXXXX` o `https://youtu.be/XXXXXXXXXXX`.
3. Guardá el archivo. No hace falta tocar ningún componente ni página.

Mientras un video siga con su placeholder, la web muestra automáticamente
un aviso de "Video todavía no disponible" en vez de romperse, así podés ir
publicando de a poco.

## 5. Agregar una meditación nueva

Todo el contenido sale de **`src/data/meditations.js`**. Para sumar una
meditación:

1. Copiá un objeto completo del array `MEDITATIONS`.
2. Cambiale el `id` (único, formato sugerido `categoria-nivel`, por ejemplo
   `calma-4`).
3. Completá `title`, `category` (debe ser un `slug` válido de
   `src/data/categories.js`), `level` (1, 2 o 3), `duration` (en minutos),
   `description`, `youtubeUrl` (placeholder o real) y `order`.
4. Si pertenece al Desafío de 10 días, poné el número de día en
   `challengeDay`; si no, dejalo en `null`.

No hace falta modificar ningún componente: las tarjetas, los filtros, el
buscador y la página de detalle se generan automáticamente a partir de ese
archivo. La arquitectura está pensada para soportar cientos de meditaciones
sin cambios de diseño.

### Agregar una categoría nueva

Poco frecuente, pero si hace falta: agregá un objeto en
`src/data/categories.js` (slug, name, objective, order) y sumale un tema
visual (degradé + ícono) en `src/components/CategoryVisual.jsx`.

### Editar el Desafío de 10 días

La estructura vive en `src/data/challenge.js`. Cada día referencia una
meditación existente por `meditationId` — la categoría y la duración que se
muestran se toman siempre de esa meditación, así nunca quedan
desincronizadas.

## 6. Modificar textos

Los textos de marca (hero de la home, "Antes de empezar", mensaje de cierre
del desafío, footer, etc.) están directamente en los archivos de
`src/app/**/page.js` y `src/app/**/*.jsx` correspondientes a cada pantalla,
como texto plano dentro del JSX — buscalos por el texto en español y
editalos ahí mismo.

## 7. Cambiar imágenes / estilo visual

Por ahora las categorías usan fondos generados (degradé de marca + un
ícono lineal minimalista) en vez de fotografía, definidos en
`src/components/CategoryVisual.jsx`. Esto mantiene la web liviana y evita
el cliché de fotos de yoga genéricas.

Para pasar a fotografía real en el futuro: agregá las imágenes a
`public/`, y dentro de `CategoryVisual.jsx` reemplazá el fondo de degradé
por un `<Image>` de `next/image` para la categoría correspondiente.

La paleta de colores y las tipografías están centralizadas en
`tailwind.config.js` (colores) y `src/app/layout.js` (tipografías, vía
`next/font/google`).

## 8. Publicar en Vercel

1. Subí el proyecto a un repositorio de GitHub (este mismo repo sirve).
2. Entrá a [vercel.com](https://vercel.com/) → **Add New Project** →
   importá el repositorio.
3. Como el proyecto vive en la carpeta `moturi-meditaciones/` dentro del
   repo, en **Root Directory** seleccioná `moturi-meditaciones`.
4. Vercel detecta Next.js automáticamente (Build Command `next build`,
   Output `.next`) — no hace falta tocar nada más.
5. Deploy. Cada push a la rama principal genera un nuevo deploy
   automáticamente.

## 9. Conectar un dominio propio

Pensado para publicarse en un subdominio como `meditaciones.moturi.com` o
`meditar.moturi.com`:

1. En el proyecto de Vercel, andá a **Settings → Domains**.
2. Agregá el subdominio deseado.
3. Vercel te va a pedir crear un registro `CNAME` (o `A`, según el caso)
   en el DNS del dominio `moturi.com` apuntando a Vercel.
4. Una vez propagado el DNS, el subdominio queda activo automáticamente
   con HTTPS.

No hace falta hacer nada más en el código: el proyecto ya está preparado
para funcionar en cualquier dominio o subdominio.

## Estructura del proyecto

```
moturi-meditaciones/
├── public/                          # Logo y assets estáticos (ver sección 3)
├── src/
│   ├── app/                         # Rutas (Next.js App Router)
│   │   ├── layout.js                 # Layout raíz, fuentes, metadata global
│   │   ├── page.js                   # Home
│   │   ├── icon.js                   # Favicon generado
│   │   ├── opengraph-image.js        # Imagen para compartir en redes
│   │   ├── sitemap.js / robots.js    # SEO
│   │   ├── meditaciones/
│   │   │   ├── page.js               # Biblioteca completa (filtros + buscador)
│   │   │   ├── MeditationsExplorer.jsx
│   │   │   └── [id]/page.js          # Página de una meditación
│   │   └── desafio-10-dias/
│   │       ├── page.js               # Overview del desafío + progreso
│   │       ├── ChallengeOverview.jsx
│   │       └── [day]/page.js         # Página de un día del desafío
│   ├── components/                  # Componentes reutilizables
│   │   ├── Navbar.jsx, Footer.jsx, Logo.jsx, BackButton.jsx
│   │   ├── MeditationCard.jsx, CategoryCard.jsx, CategoryVisual.jsx
│   │   ├── VideoPlayer.jsx, LevelBadge.jsx, DurationBadge.jsx
│   │   ├── ProgressBar.jsx, ChallengeDay.jsx
│   │   └── FilterBar.jsx, SearchBar.jsx, MoodCheck.jsx
│   ├── data/                        # ← Toda la información de contenido vive acá
│   │   ├── meditations.js            # Las 24 meditaciones (fuente única de verdad)
│   │   ├── categories.js             # Las 8 categorías
│   │   ├── levels.js                 # Los 3 niveles
│   │   └── challenge.js              # Los 10 días del desafío
│   └── lib/                         # Lógica auxiliar
│       ├── youtube.js                # Parseo de URLs / thumbnails de YouTube
│       ├── format.js                 # Formato de duración, buckets de filtro
│       ├── filterMeditations.js      # Lógica de filtros + búsqueda
│       └── progress.js               # Progreso del desafío en localStorage
├── tailwind.config.js                # Paleta de colores y tipografías de marca
└── next.config.mjs
```

## Rendimiento y accesibilidad (ya resuelto)

- **Sin embeds pesados en la Home**: los videos de YouTube solo se cargan
  cuando el usuario toca "Reproducir" en la página de cada meditación
  (antes de eso se muestra solo una miniatura liviana).
- **Mobile-first**: pensado para abrirse desde un QR en el celular
  (botones grandes, sin scroll horizontal, menú simple).
- Navegación por teclado, `alt`/`aria-label` en elementos interactivos,
  buen contraste de color y respeto a `prefers-reduced-motion`.
- Sin login, sin cuentas, sin backend: entrar, elegir y escuchar.

## Nota sobre esta entrega

Este proyecto se construyó y revisó línea por línea (estructura, imports,
sintaxis JSX y consistencia de datos verificadas), pero el entorno en el
que se generó no tuvo acceso a `registry.npmjs.org`, así que **no se pudo
correr `npm install` / `npm run build` de forma automática antes de
entregarlo**. Antes de publicar en producción, corré localmente:

```bash
npm install
npm run build
```

y avisame si aparece algún error para corregirlo.
