import Link from "next/link";
import Logo from "@/components/Logo";
import CategoryCard from "@/components/CategoryCard";
import CategoryVisual from "@/components/CategoryVisual";
import LevelBadge from "@/components/LevelBadge";
import DurationBadge from "@/components/DurationBadge";
import { CATEGORIES } from "@/data/categories";
import { getMeditationById } from "@/data/meditations";

const STARTER_MEDITATION_ID = "calma-1";

export default function HomePage() {
  const starter = getMeditationById(STARTER_MEDITATION_ID);

  return (
    <>
      {/* Hero */}
      <section className="mx-auto max-w-content px-4 pb-10 pt-14 text-center sm:px-6 sm:pt-20">
        <Logo className="text-2xl" />
        <h1 className="mt-6 font-display text-4xl font-semibold tracking-tight text-ink sm:text-5xl">
          Meditaciones
        </h1>
        <p className="mx-auto mt-4 max-w-md text-lg text-ink-soft">
          Un espacio para frenar, respirar y volver a vos.
        </p>
        <p className="mt-10 font-display text-xl text-ink sm:text-2xl">¿Qué necesitás hoy?</p>
      </section>

      {/* Categorías */}
      <section className="mx-auto max-w-content px-4 sm:px-6" aria-label="Categorías de meditación">
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 sm:gap-4 lg:grid-cols-4">
          {CATEGORIES.map((category) => (
            <CategoryCard key={category.slug} category={category} />
          ))}
        </div>
      </section>

      {/* Desafío de 10 días */}
      <section className="mx-auto max-w-content px-4 py-14 sm:px-6 sm:py-20">
        <Link
          href="/desafio-10-dias"
          className="group relative flex flex-col overflow-hidden rounded-xl2 border border-line bg-moturi shadow-soft transition-transform duration-300 ease-calm hover:-translate-y-1 focus-visible:-translate-y-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi-mist md:flex-row md:items-center"
        >
          <div className="flex flex-1 flex-col gap-3 p-8 sm:p-10">
            <span className="w-fit rounded-full bg-surface/15 px-3 py-1 text-xs font-medium uppercase tracking-wide text-moturi-mist">
              Experiencia guiada
            </span>
            <h2 className="font-display text-3xl font-semibold text-surface sm:text-4xl">
              Desafío de 10 días
            </h2>
            <p className="max-w-md text-surface/85">
              10 días para empezar a construir el hábito de detenerte unos minutos y volver a vos.
            </p>
            <span className="mt-2 inline-flex w-fit items-center gap-1.5 rounded-full bg-surface px-5 py-2.5 text-sm font-semibold text-moturi transition-transform group-hover:scale-[1.03]">
              Empezar el desafío →
            </span>
          </div>
          <div className="hidden h-full min-h-[220px] w-full max-w-xs items-center justify-center bg-moturi-deep/40 p-8 md:flex">
            <div className="grid grid-cols-5 gap-2" aria-hidden="true">
              {Array.from({ length: 10 }).map((_, index) => (
                <span
                  key={index}
                  className="h-6 w-6 rounded-full border border-surface/40 bg-surface/10"
                />
              ))}
            </div>
          </div>
        </Link>
      </section>

      {/* Si no sabés por dónde empezar */}
      {starter && (
        <section className="mx-auto max-w-content px-4 pb-20 sm:px-6">
          <div className="flex flex-col gap-6 rounded-xl2 border border-line bg-surface p-6 shadow-card sm:flex-row sm:items-center sm:p-8">
            <CategoryVisual
              slug={starter.category}
              className="h-24 w-full shrink-0 rounded-xl sm:h-28 sm:w-28"
            />
            <div className="flex-1">
              <p className="text-xs font-medium uppercase tracking-wide text-muted">
                Si no sabés por dónde empezar
              </p>
              <h2 className="mt-1 font-display text-xl font-semibold text-ink">
                {starter.title}
              </h2>
              <div className="mt-2 flex flex-wrap gap-2">
                <LevelBadge level={starter.level} />
                <DurationBadge minutes={starter.duration} />
              </div>
            </div>
            <Link
              href={`/meditaciones/${starter.id}`}
              className="inline-flex shrink-0 items-center justify-center rounded-full bg-moturi px-6 py-3 text-sm font-semibold text-surface transition-transform hover:scale-[1.02] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi/40"
            >
              Empezar ahora
            </Link>
          </div>
        </section>
      )}
    </>
  );
}
