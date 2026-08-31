export function formatDuration(minutes) {
  return `${minutes} min`;
}

export const DURATION_BUCKETS = [
  { id: "short", label: "Hasta 5 minutos", test: (min) => min <= 5 },
  { id: "medium", label: "6–7 minutos", test: (min) => min >= 6 && min <= 7 },
  { id: "long", label: "8–10 minutos", test: (min) => min >= 8 && min <= 10 },
];

export function getDurationBucket(minutes) {
  return DURATION_BUCKETS.find((bucket) => bucket.test(minutes));
}
