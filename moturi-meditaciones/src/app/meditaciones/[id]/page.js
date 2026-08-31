import { notFound } from "next/navigation";
import BackButton from "@/components/BackButton";
import VideoPlayer from "@/components/VideoPlayer";
import LevelBadge from "@/components/LevelBadge";
import DurationBadge from "@/components/DurationBadge";
import MoodCheck from "@/components/MoodCheck";
import { MEDITATIONS, getMeditationById } from "@/data/meditations";
import { getCategoryBySlug } from "@/data/categories";

export function generateStaticParams() {
  return MEDITATIONS.map((meditation) => ({ id: meditation.id }));
}

export function generateMetadata({ params }) {
  const meditation = getMeditationById(params.id);
  if (!meditation) return {};

  return {
    title: meditation.title,
    description: meditation.description,
  };
}

export default function MeditationPage({ params }) {
  const meditation = getMeditationById(params.id);
  if (!meditation) notFound();

  const category = getCategoryBySlug(meditation.category);

  return (
    <section className="mx-auto max-w-3xl px-4 py-8 sm:px-6 sm:py-12">
      <BackButton href="/meditaciones" label="Meditaciones" className="mb-6" />

      <p className="text-xs font-medium uppercase tracking-wide text-muted">{category?.name}</p>
      <h1 className="mt-1 font-display text-3xl font-semibold text-ink sm:text-4xl">
        {meditation.title}
      </h1>

      <div className="mt-3 flex flex-wrap gap-2">
        <LevelBadge level={meditation.level} />
        <DurationBadge minutes={meditation.duration} />
      </div>

      <p className="mt-4 max-w-xl text-ink-soft">{meditation.description}</p>

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

      <div className="mt-8">
        <MoodCheck />
      </div>
    </section>
  );
}
