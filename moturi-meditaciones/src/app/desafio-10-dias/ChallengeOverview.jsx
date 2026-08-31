"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import ChallengeDay from "@/components/ChallengeDay";
import ProgressBar from "@/components/ProgressBar";
import { CHALLENGE } from "@/data/challenge";
import { getMeditationById } from "@/data/meditations";
import { CHALLENGE_TOTAL_DAYS, getCompletedDays } from "@/lib/progress";

export default function ChallengeOverview() {
  const [completedDays, setCompletedDays] = useState([]);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setCompletedDays(getCompletedDays());
    setHydrated(true);
  }, []);

  const completedCount = completedDays.length;
  const finished = hydrated && completedCount >= CHALLENGE_TOTAL_DAYS;

  return (
    <section className="mx-auto max-w-content px-4 py-10 sm:px-6 sm:py-14">
      <div className="mx-auto max-w-2xl text-center">
        <h1 className="font-display text-3xl font-semibold text-ink sm:text-4xl">
          Desafío de 10 días
        </h1>
        <p className="mt-3 text-ink-soft">
          10 días para empezar a construir el hábito de detenerte unos minutos y volver a vos.
        </p>
      </div>

      <div className="mx-auto mt-8 max-w-md">
        <div className="flex items-center justify-between text-sm font-medium text-ink-soft">
          <span>{hydrated ? completedCount : 0} de {CHALLENGE_TOTAL_DAYS} días completados</span>
        </div>
        <ProgressBar value={hydrated ? completedCount : 0} total={CHALLENGE_TOTAL_DAYS} className="mt-2" />
      </div>

      {finished && (
        <div className="mx-auto mt-10 max-w-xl rounded-xl2 border border-sage/30 bg-sage/10 p-8 text-center">
          <h2 className="font-display text-2xl font-semibold text-ink">
            Completaste el desafío.
          </h2>
          <p className="mt-3 text-ink-soft">
            Durante 10 días elegiste detenerte, observar y volver a vos. El objetivo nunca fue
            hacerlo perfecto, sino empezar a construir el hábito.
          </p>
          <Link
            href="/meditaciones"
            className="mt-5 inline-flex items-center justify-center rounded-full bg-moturi px-6 py-3 text-sm font-semibold text-surface transition-transform hover:scale-[1.02] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi/40"
          >
            Seguir explorando meditaciones
          </Link>
        </div>
      )}

      <div className="mt-10 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {CHALLENGE.map((day) => {
          const meditation = getMeditationById(day.meditationId);
          if (!meditation) return null;
          return (
            <ChallengeDay
              key={day.day}
              day={day}
              meditation={meditation}
              completed={hydrated && completedDays.includes(day.day)}
            />
          );
        })}
      </div>
    </section>
  );
}
