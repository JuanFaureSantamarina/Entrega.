/**
 * Los 3 niveles de progresión dentro de cada categoría.
 * No es un sistema de dificultad: es una progresión natural de la práctica.
 */
export const LEVELS = [
  {
    level: 1,
    name: "Iniciar",
    description: "Meditaciones simples y más guiadas, pensadas para alguien que recién empieza.",
    durationRange: "3–5 min",
  },
  {
    level: 2,
    name: "Profundizar",
    description: "Mayor espacio de observación y algunos silencios más largos.",
    durationRange: "5–7 min",
  },
  {
    level: 3,
    name: "Integrar",
    description: "Menos instrucciones y mayor autonomía, con más espacio de silencio e introspección.",
    durationRange: "8–10 min",
  },
];

export function getLevel(level) {
  return LEVELS.find((item) => item.level === level);
}
