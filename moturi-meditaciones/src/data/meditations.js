/**
 * Fuente única de verdad para todas las meditaciones de la biblioteca.
 *
 * Cómo agregar una meditación nueva:
 * 1. Copiá un objeto completo de este archivo.
 * 2. Cambiá `id` por uno nuevo y único (formato sugerido: "categoria-nivel", o
 *    "categoria-nivel-b" si ya existe una combinación igual).
 * 3. Completá título, categoría (debe ser un `slug` de src/data/categories.js),
 *    nivel (1, 2 o 3), duración en minutos, descripción y `youtubeUrl`.
 * 4. Si pertenece al Desafío de 10 días, marcá `challengeDay` con el número de
 *    día (1 a 10); si no, dejalo en `null`.
 * 5. No hace falta tocar ningún componente ni página: las tarjetas, filtros,
 *    el buscador y el desafío se generan automáticamente desde este archivo.
 *
 * Reemplazo de links de YouTube:
 * Buscá el texto "YOUTUBE_URL_REEMPLAZAR" en este archivo — cada meditación
 * tiene un placeholder único e identificable en el campo `youtubeUrl`.
 * Pegá ahí la URL real del video (formato https://www.youtube.com/watch?v=...
 * o https://youtu.be/...). Mientras el placeholder siga ahí, la web muestra
 * un aviso de "video no disponible todavía" en vez de romperse.
 *
 * Campo `image`: por ahora usamos una imagen generada por categoría
 * (ver src/components/CategoryVisual.jsx). Si en el futuro querés una imagen
 * específica para una meditación puntual, agregá un campo `image` con la
 * ruta (ej: "/meditaciones/calma-1.jpg") y usalo en MeditationCard.
 */

export const MEDITATIONS = [
  // ---------- CALMA ----------
  {
    id: "calma-1",
    title: "Volver a la respiración",
    category: "calma",
    level: 1,
    duration: 4,
    description:
      "Una práctica breve para detenerte, observar tu respiración y bajar el ritmo.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_CALMA_NIVEL_1",
    order: 1,
    challengeDay: 1,
  },
  {
    id: "calma-2",
    title: "Bajar el ruido",
    category: "calma",
    level: 2,
    duration: 6,
    description:
      "Un espacio para aquietar la mente y soltar el ruido acumulado del día.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_CALMA_NIVEL_2",
    order: 2,
    challengeDay: 6,
  },
  {
    id: "calma-3",
    title: "Soltar tensión",
    category: "calma",
    level: 3,
    duration: 9,
    description:
      "Una práctica más larga para reconocer dónde sostenés tensión y permitir que se libere.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_CALMA_NIVEL_3",
    order: 3,
    challengeDay: null,
  },

  // ---------- ENFOQUE ----------
  {
    id: "enfoque-1",
    title: "Una cosa a la vez",
    category: "enfoque",
    level: 1,
    duration: 4,
    description:
      "Una guía simple para entrenar la atención y hacer una sola cosa genuinamente a la vez.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_ENFOQUE_NIVEL_1",
    order: 1,
    challengeDay: 3,
  },
  {
    id: "enfoque-2",
    title: "Limpiar la atención",
    category: "enfoque",
    level: 2,
    duration: 6,
    description:
      "Un ejercicio para despejar la mente dispersa y recuperar foco antes de seguir con el día.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_ENFOQUE_NIVEL_2",
    order: 2,
    challengeDay: null,
  },
  {
    id: "enfoque-3",
    title: "Claridad antes de actuar",
    category: "enfoque",
    level: 3,
    duration: 9,
    description: "Un espacio de silencio para ordenar ideas y actuar con más claridad.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_ENFOQUE_NIVEL_3",
    order: 3,
    challengeDay: null,
  },

  // ---------- SUEÑO ----------
  {
    id: "sueno-1",
    title: "Cerrar el día",
    category: "sueno",
    level: 1,
    duration: 5,
    description:
      "Una práctica guiada para marcar el cierre del día y preparar el cuerpo para descansar.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_SUENO_NIVEL_1",
    order: 1,
    challengeDay: null,
  },
  {
    id: "sueno-2",
    title: "Relajación corporal",
    category: "sueno",
    level: 2,
    duration: 7,
    description:
      "Un recorrido lento por el cuerpo para soltar tensión acumulada antes de dormir.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_SUENO_NIVEL_2",
    order: 2,
    challengeDay: null,
  },
  {
    id: "sueno-3",
    title: "Soltar pensamientos",
    category: "sueno",
    level: 3,
    duration: 10,
    description:
      "Un espacio extenso de calma para dejar ir los pensamientos del día y descansar mejor.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_SUENO_NIVEL_3",
    order: 3,
    challengeDay: null,
  },

  // ---------- PRESENCIA ----------
  {
    id: "presencia-1",
    title: "Cinco sentidos",
    category: "presencia",
    level: 1,
    duration: 4,
    description:
      "Un ejercicio simple para volver al presente a través de lo que ves, escuchás y sentís.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_PRESENCIA_NIVEL_1",
    order: 1,
    challengeDay: 2,
  },
  {
    id: "presencia-2",
    title: "Escaneo corporal",
    category: "presencia",
    level: 2,
    duration: 6,
    description:
      "Un recorrido consciente por el cuerpo para reconectar con el momento actual.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_PRESENCIA_NIVEL_2",
    order: 2,
    challengeDay: null,
  },
  {
    id: "presencia-3",
    title: "Estar acá",
    category: "presencia",
    level: 3,
    duration: 9,
    description:
      "Una práctica de mayor silencio para sostener la atención en el presente sin esfuerzo.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_PRESENCIA_NIVEL_3",
    order: 3,
    challengeDay: null,
  },

  // ---------- AUTOCONCEPTO ----------
  {
    id: "autoconcepto-1",
    title: "Cómo me hablo",
    category: "autoconcepto",
    level: 1,
    duration: 5,
    description: "Una práctica para observar el diálogo interno sin juzgarlo, solo notarlo.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_AUTOCONCEPTO_NIVEL_1",
    order: 1,
    challengeDay: 5,
  },
  {
    id: "autoconcepto-2",
    title: "La persona que estoy construyendo",
    category: "autoconcepto",
    level: 2,
    duration: 7,
    description:
      "Un espacio para reflexionar sobre las decisiones y hábitos que te están formando.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_AUTOCONCEPTO_NIVEL_2",
    order: 2,
    challengeDay: 9,
  },
  {
    id: "autoconcepto-3",
    title: "Identidad y elección",
    category: "autoconcepto",
    level: 3,
    duration: 10,
    description:
      "Una práctica de mayor silencio para conectar con quién querés ser y por qué.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_AUTOCONCEPTO_NIVEL_3",
    order: 3,
    challengeDay: null,
  },

  // ---------- EMOCIONES ----------
  {
    id: "emociones-1",
    title: "Nombrar lo que siento",
    category: "emociones",
    level: 1,
    duration: 4,
    description: "Una práctica breve para identificar una emoción sin necesidad de resolverla.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_EMOCIONES_NIVEL_1",
    order: 1,
    challengeDay: 4,
  },
  {
    id: "emociones-2",
    title: "Antes de reaccionar",
    category: "emociones",
    level: 2,
    duration: 6,
    description: "Un espacio para crear distancia entre lo que sentís y cómo respondés.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_EMOCIONES_NIVEL_2",
    order: 2,
    challengeDay: null,
  },
  {
    id: "emociones-3",
    title: "Atravesar un momento difícil",
    category: "emociones",
    level: 3,
    duration: 9,
    description:
      "Una práctica más profunda para acompañarte durante un momento emocional intenso.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_EMOCIONES_NIVEL_3",
    order: 3,
    challengeDay: null,
  },

  // ---------- ENERGÍA ----------
  {
    id: "energia-1",
    title: "Activar el día",
    category: "energia",
    level: 1,
    duration: 3,
    description: "Una práctica corta para despertar el cuerpo y empezar el día con intención.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_ENERGIA_NIVEL_1",
    order: 1,
    challengeDay: null,
  },
  {
    id: "energia-2",
    title: "Reiniciar",
    category: "energia",
    level: 2,
    duration: 6,
    description:
      "Un espacio para soltar lo que quedó del momento anterior y volver a empezar.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_ENERGIA_NIVEL_2",
    order: 2,
    challengeDay: 8,
  },
  {
    id: "energia-3",
    title: "Dirección",
    category: "energia",
    level: 3,
    duration: 8,
    description:
      "Una práctica más profunda para conectar energía, intención y hacia dónde querés ir.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_ENERGIA_NIVEL_3",
    order: 3,
    challengeDay: 10,
  },

  // ---------- GRATITUD ----------
  {
    id: "gratitud-1",
    title: "Tres cosas",
    category: "gratitud",
    level: 1,
    duration: 4,
    description:
      "Una práctica simple para reconocer tres cosas buenas del día, por pequeñas que parezcan.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_GRATITUD_NIVEL_1",
    order: 1,
    challengeDay: null,
  },
  {
    id: "gratitud-2",
    title: "Lo cotidiano",
    category: "gratitud",
    level: 2,
    duration: 6,
    description: "Un espacio para notar y valorar lo que normalmente pasa desapercibido.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_GRATITUD_NIVEL_2",
    order: 2,
    challengeDay: 7,
  },
  {
    id: "gratitud-3",
    title: "Perspectiva",
    category: "gratitud",
    level: 3,
    duration: 9,
    description: "Una práctica de mayor silencio para ampliar la mirada sobre lo que tenés.",
    youtubeUrl: "YOUTUBE_URL_REEMPLAZAR_GRATITUD_NIVEL_3",
    order: 3,
    challengeDay: null,
  },
];

export function getMeditationById(id) {
  return MEDITATIONS.find((meditation) => meditation.id === id);
}

export function getMeditationsByCategory(categorySlug) {
  return MEDITATIONS.filter((meditation) => meditation.category === categorySlug).sort(
    (a, b) => a.order - b.order
  );
}
