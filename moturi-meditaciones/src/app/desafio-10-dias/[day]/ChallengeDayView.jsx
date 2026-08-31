"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import BackButton from "@/components/BackButton";
import VideoPlayer from "@/components/VideoPlayer";
import LevelBadge from "@/components/LevelBadge";
import DurationBadge from "@/components/DurationBadge";
import MoodCheck from "@/components/MoodCheck";
import { getCategoryBySlug } from "@/data/categories";
import { CHALLENGE_TOTAL_DAYS, isDayCompleted, toggleDayCompleted } from "@/lib/progress";

export default function ChallengeDayView({ day, meditation }) {
  const [completed, setCompleted] = useState(false);
  const [hydrated, setHydrated] = useState(false);
  const category = getCategoryBySlug(meditation.category);
  const isLastDay = day.day === CHALLENGE_TOTAL_DAYS;

  useEffect(() => {
    setCompleted(isDayCompleted(day.day));
    setHydrated(true);
  }, [day.day]);

  function handleToggle() {
    const updated = toggleDayCompleted(day.day);
    setCompleted(updated.includes(day.day));
  }

  return (
    <section className="mx-auto max-w-3xl px-4 py-8 sm:px-6 sm:py-12">
      <BackButton href="/desafio-10-dias" label="Desafío de 10 días" className="mb-6" />

      <p className="text-xs font-medium uppercase tracking-wide text-muted">
        Día {day.day} de {CHALLENGE_TOTAL_DAYS} · {category?.name}
      </p>
      <h1 className="mt-1 font-display text-3xl font-semibold text-ink sm:text-4xl">
        {day.title}
      </h1>

      <div className="mt-3 flex flex-wrap gap-2">
        <LevelBadge level={meditation.level} />
        <DurationBadge minutes={meditation.duration} />
      </div>

      <p className="mt-4 max-w-xl text-ink-soft">{day.objective}</p>

      <div className="mt-6 rounded-xl2 border border-line bg-mist/60 p-4 text-sm text-ink-soft">
        <p className="font-medium text-ink">Antes de empezar</p>
        <p className="mt-1">
          Buscá una posición cómoda. Podés sentarte o acostarte dependiendo de la práctica. No
          necesitás hacer nada perfecto. Simplemente escuchá y seguí la guía.
        </p>
      </div>

      <div className="mt-6">
        <VideoPlayer
          youtubeUrl={meditation.youtubeUrl}
          category={meditation.category}
          title={meditation.title}
        />
      </div>

      <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <button
          type="button"
          onClick={handleToggle}
          disabled={!hydrated}
          className={`inline-flex items-center justify-center gap-2 rounded-full px-6 py-3 text-sm font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi/40 ${
            completed
              ? "bg-sage text-surface hover:bg-sage/90"
              : "bg-moturi text-surface hover:bg-moturi-deep"
          }`}
        >
          {completed ? "✓ Día completado" : "Marcar como completado"}
        </button>

        {!isLastDay && (
          <Link
            href={`/desafio-10-dias/${day.day + 1}`}
            className="inline-flex items-center justify-center gap-1.5 rounded-full border border-line bg-surface px-5 py-3 text-sm font-medium text-ink-soft transition-colors hover:text-ink focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi/40"
          >
            Día siguiente →
          </Link>
        )}
      </div>

      <div className="mt-8">
        <MoodCheck />
      </div>
    </section>
  );
}
