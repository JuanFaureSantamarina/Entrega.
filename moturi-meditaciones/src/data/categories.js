/**
 * Categorías de la biblioteca de meditaciones.
 *
 * Para agregar una categoría nueva: copiá un objeto, cambiá el `slug`
 * (se usa en las URLs y para vincular meditaciones vía `category`),
 * y sumale un tema visual en `src/components/CategoryVisual.jsx`.
 */
export const CATEGORIES = [
  {
    slug: "calma",
    name: "Calma",
    objective: "Bajar la activación, el estrés y el ruido mental.",
    order: 1,
  },
  {
    slug: "enfoque",
    name: "Enfoque",
    objective: "Recuperar concentración y claridad mental.",
    order: 2,
  },
  {
    slug: "sueno",
    name: "Sueño",
    objective: "Desacelerar, soltar el día y facilitar el descanso.",
    order: 3,
  },
  {
    slug: "presencia",
    name: "Presencia",
    objective: "Volver al cuerpo y al momento actual.",
    order: 4,
  },
  {
    slug: "autoconcepto",
    name: "Autoconcepto",
    objective:
      "Trabajar identidad, diálogo interno y la persona que estamos construyendo.",
    order: 5,
  },
  {
    slug: "emociones",
    name: "Emociones",
    objective: "Observar lo que sentimos y crear espacio antes de reaccionar.",
    order: 6,
  },
  {
    slug: "energia",
    name: "Energía",
    objective: "Empezar o reiniciar el día con intención.",
    order: 7,
  },
  {
    slug: "gratitud",
    name: "Gratitud",
    objective:
      "Entrenar perspectiva y reconocimiento de aquello que muchas veces damos por sentado.",
    order: 8,
  },
];

export function getCategoryBySlug(slug) {
  return CATEGORIES.find((category) => category.slug === slug);
}
