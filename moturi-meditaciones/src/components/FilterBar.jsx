import { CATEGORIES } from "@/data/categories";
import { LEVELS } from "@/data/levels";
import { DURATION_BUCKETS } from "@/lib/format";

function Pill({ active, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={`shrink-0 rounded-full border px-3.5 py-1.5 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi/40 ${
        active
          ? "border-moturi bg-moturi text-surface"
          : "border-line bg-surface text-ink-soft hover:border-moturi/40 hover:text-ink"
      }`}
    >
      {children}
    </button>
  );
}

export default function FilterBar({ filters, onChange, onReset }) {
  const { category, level, duration } = filters;
  const hasActiveFilters = Boolean(category || level || duration);

  return (
    <div className="flex flex-col gap-3">
      <div className="-mx-4 flex gap-2 overflow-x-auto px-4 pb-1 sm:mx-0 sm:flex-wrap sm:px-0">
        <Pill active={!category} onClick={() => onChange({ category: null })}>
          Todas las categorías
        </Pill>
        {CATEGORIES.map((cat) => (
          <Pill
            key={cat.slug}
            active={category === cat.slug}
            onClick={() => onChange({ category: category === cat.slug ? null : cat.slug })}
          >
            {cat.name}
          </Pill>
        ))}
      </div>

      <div className="-mx-4 flex gap-2 overflow-x-auto px-4 pb-1 sm:mx-0 sm:flex-wrap sm:px-0">
        {LEVELS.map((lvl) => (
          <Pill
            key={lvl.level}
            active={level === lvl.level}
            onClick={() => onChange({ level: level === lvl.level ? null : lvl.level })}
          >
            Nivel {lvl.level} · {lvl.name}
          </Pill>
        ))}
        <span className="mx-1 h-6 w-px shrink-0 self-center bg-line" aria-hidden="true" />
        {DURATION_BUCKETS.map((bucket) => (
          <Pill
            key={bucket.id}
            active={duration === bucket.id}
            onClick={() => onChange({ duration: duration === bucket.id ? null : bucket.id })}
          >
            {bucket.label}
          </Pill>
        ))}
      </div>

      {hasActiveFilters && (
        <button
          type="button"
          onClick={onReset}
          className="self-start text-sm font-medium text-moturi underline-offset-2 hover:underline"
        >
          Limpiar filtros
        </button>
      )}
    </div>
  );
}
