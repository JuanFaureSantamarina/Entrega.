import Link from "next/link";
import CategoryVisual from "./CategoryVisual";
import LevelBadge from "./LevelBadge";
import DurationBadge from "./DurationBadge";
import { getCategoryBySlug } from "@/data/categories";

export default function MeditationCard({ meditation }) {
  const category = getCategoryBySlug(meditation.category);

  return (
    <Link
      href={`/meditaciones/${meditation.id}`}
      className="group flex gap-4 rounded-xl2 border border-line bg-surface p-3 shadow-card transition-all duration-300 ease-calm hover:-translate-y-0.5 hover:shadow-soft focus-visible:-translate-y-0.5 focus-visible:shadow-soft focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi/40 sm:p-4"
    >
      <CategoryVisual
        slug={meditation.category}
        className="h-20 w-20 shrink-0 rounded-lg sm:h-24 sm:w-24"
      />

      <div className="flex min-w-0 flex-1 flex-col justify-between gap-2">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-muted">
            {category?.name}
          </p>
          <h3 className="mt-0.5 truncate font-display text-base font-semibold text-ink sm:text-lg">
            {meditation.title}
          </h3>
          <p className="mt-1 line-clamp-2 text-sm text-ink-soft">{meditation.description}</p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <LevelBadge level={meditation.level} />
          <DurationBadge minutes={meditation.duration} />
          <span className="ml-auto shrink-0 text-sm font-semibold text-moturi transition-colors group-hover:text-moturi-deep">
            Escuchar →
          </span>
        </div>
      </div>
    </Link>
  );
}
