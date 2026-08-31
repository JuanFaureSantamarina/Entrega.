/**
 * Estructura del Desafío de 10 días.
 *
 * Cada día referencia una meditación existente de src/data/meditations.js
 * mediante `meditationId` — la categoría y la duración se toman siempre de
 * esa meditación, así nunca quedan desincronizadas. `title` y `objective`
 * son específicos del desafío (el marco narrativo del día), distintos del
 * título de la meditación en sí.
 *
 * Importante: los días del desafío deben coincidir con el campo
 * `challengeDay` de la meditación referenciada en meditations.js.
 */
export const CHALLENGE = [
  {
    day: 1,
    title: "Empezar por respirar",
    objective:
      "Aprender a detenerse unos minutos y utilizar la respiración como punto de regreso.",
    meditationId: "calma-1",
  },
  {
    day: 2,
    title: "Volver al presente",
    objective: "Empezar a notar el entorno y salir del piloto automático.",
    meditationId: "presencia-1",
  },
  {
    day: 3,
    title: "Una cosa a la vez",
    objective: "Practicar dirigir conscientemente la atención.",
    meditationId: "enfoque-1",
  },
  {
    day: 4,
    title: "Observar lo que siento",
    objective: "Aprender a reconocer una emoción sin reaccionar automáticamente.",
    meditationId: "emociones-1",
  },
  {
    day: 5,
    title: "Cómo me estoy hablando",
    objective: "Empezar a observar el diálogo interno.",
    meditationId: "autoconcepto-1",
  },
  {
    day: 6,
    title: "Bajar el ruido",
    objective: "Crear más espacio entre los pensamientos y nuestra atención.",
    meditationId: "calma-2",
  },
  {
    day: 7,
    title: "Reconocer lo cotidiano",
    objective:
      "Entrenar la capacidad de reconocer aquello que normalmente damos por sentado.",
    meditationId: "gratitud-2",
  },
  {
    day: 8,
    title: "Reiniciar",
    objective: "Entender que cualquier momento del día puede convertirse en un nuevo comienzo.",
    meditationId: "energia-2",
  },
  {
    day: 9,
    title: "La persona que estoy construyendo",
    objective: "Reflexionar sobre las cualidades y acciones que queremos construir.",
    meditationId: "autoconcepto-2",
  },
  {
    day: 10,
    title: "Dirección",
    objective: "Cerrar el desafío conectando presencia, intención y dirección personal.",
    meditationId: "energia-3",
  },
];

export function getChallengeDay(day) {
  return CHALLENGE.find((item) => item.day === Number(day));
}
