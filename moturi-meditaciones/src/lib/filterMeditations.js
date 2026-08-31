import { getDurationBucket } from "./format";

/**
 * Filtra y busca dentro de la lista completa de meditaciones.
 * @param {Array} meditations - lista base (src/data/meditations.js)
 * @param {{ category?: string, level?: number, duration?: string, query?: string }} filters
 */
export function filterMeditations(meditations, filters = {}) {
  const { category, level, duration, query } = filters;
  const normalizedQuery = query?.trim().toLowerCase();

  return meditations.filter((meditation) => {
    if (category && meditation.category !== category) return false;
    if (level && meditation.level !== Number(level)) return false;
    if (duration) {
      const bucket = getDurationBucket(meditation.duration);
      if (bucket?.id !== duration) return false;
    }
    if (normalizedQuery) {
      const haystack = `${meditation.title} ${meditation.description}`.toLowerCase();
      if (!haystack.includes(normalizedQuery)) return false;
    }
    return true;
  });
}
