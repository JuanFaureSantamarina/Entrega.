import Link from "next/link";
import DurationBadge from "./DurationBadge";
import { getCategoryBySlug } from "@/data/categories";

export default function ChallengeDay({ day, meditation, completed }) {
  const category = getCategoryBySlug(meditation.category);

  return (
    <Link
      href={`/desafio-10-dias/${day.day}`}
      className={`group flex flex-col gap-3 rounded-xl2 border p-4 shadow-card transition-all duration-300 ease-calm hover:-translate-y-0.5 hover:shadow-soft focus-visible:-translate-y-0.5 focus-visible:shadow-soft focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi/40 ${
        completed ? "border-sage/40 bg-sage/5" : "border-line bg-surface"
      }`}
    >
      <div className="flex items-center justify-between">
        <span
          className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-sm font-semibold ${
            completed ? "bg-sage text-surface" : "bg-moturi-mist text-moturi-deep"
          }`}
          aria-hidden="true"
        >
          {completed ? (
            <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor">
              <path d="M5 10.5 8.5 14 15 6.5" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          ) : (
            day.day
          )}
        </span>
        <span className="text-xs font-medium uppercase tracking-wide text-muted">
          Día {day.day} · {category?.name}
        </span>
      </div>

      <div>
        <h3 className="font-display text-base font-semibold text-ink">{day.title}</h3>
        <p className="mt-1 text-sm text-ink-soft">{day.objective}</p>
      </div>

      <div className="mt-auto flex items-center justify-between pt-1">
        <DurationBadge minutes={meditation.duration} />
        <span className="text-sm font-semibold text-moturi transition-colors group-hover:text-moturi-deep">
          {completed ? "Repasar" : "Comenzar"} →
        </span>
      </div>
    </Link>
  );
}
