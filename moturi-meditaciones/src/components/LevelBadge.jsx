import { getLevel } from "@/data/levels";

export default function LevelBadge({ level, className = "" }) {
  const info = getLevel(level);
  if (!info) return null;

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full bg-moturi-mist px-2.5 py-1 text-xs font-medium text-moturi-deep ${className}`}
    >
      Nivel {info.level} · {info.name}
    </span>
  );
}
