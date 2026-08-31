"use client";

import { useState } from "react";
import { getYoutubeEmbedUrl, getYoutubeThumbnailUrl, isPlaceholderUrl } from "@/lib/youtube";
import CategoryVisual from "./CategoryVisual";

/**
 * Reproductor de YouTube embebido, con carga diferida (facade pattern):
 * mientras el usuario no toca "Reproducir", solo se muestra una miniatura
 * liviana. El iframe de YouTube recién se monta al hacer clic, para no
 * cargar reproductores pesados que el usuario nunca llega a usar.
 */
export default function VideoPlayer({ youtubeUrl, category, title }) {
  const [playing, setPlaying] = useState(false);
  const [thumbnailError, setThumbnailError] = useState(false);

  const embedUrl = getYoutubeEmbedUrl(youtubeUrl);
  const thumbnailUrl = getYoutubeThumbnailUrl(youtubeUrl);
  const notConfigured = isPlaceholderUrl(youtubeUrl);

  if (notConfigured) {
    return (
      <div className="flex aspect-video w-full flex-col items-center justify-center gap-2 rounded-xl2 border border-dashed border-line bg-mist px-6 text-center">
        <p className="font-medium text-ink-soft">Video todavía no disponible</p>
        <p className="max-w-sm text-sm text-muted">
          Reemplazá el placeholder <code className="rounded bg-surface px-1.5 py-0.5">{youtubeUrl}</code>{" "}
          por el link real de YouTube en <code className="rounded bg-surface px-1.5 py-0.5">src/data/meditations.js</code>.
        </p>
      </div>
    );
  }

  if (playing && embedUrl) {
    return (
      <div className="aspect-video w-full overflow-hidden rounded-xl2 bg-ink shadow-soft">
        <iframe
          src={embedUrl}
          title={title}
          className="h-full w-full"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
      </div>
    );
  }

  return (
    <button
      type="button"
      onClick={() => setPlaying(true)}
      className="group relative block aspect-video w-full overflow-hidden rounded-xl2 shadow-soft focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi/50"
      aria-label={`Reproducir meditación: ${title}`}
    >
      {thumbnailUrl && !thumbnailError ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={thumbnailUrl}
          alt=""
          className="h-full w-full object-cover"
          loading="lazy"
          onError={() => setThumbnailError(true)}
        />
      ) : (
        <CategoryVisual slug={category} size="hero" className="h-full w-full" />
      )}

      <div className="absolute inset-0 bg-ink/25 transition-colors group-hover:bg-ink/35" />

      <span className="absolute inset-0 flex items-center justify-center">
        <span className="flex h-16 w-16 items-center justify-center rounded-full bg-surface/95 shadow-soft transition-transform duration-300 ease-calm group-hover:scale-105">
          <svg viewBox="0 0 24 24" className="ml-1 h-6 w-6 text-moturi" fill="currentColor" aria-hidden="true">
            <path d="M8 5v14l11-7Z" />
          </svg>
        </span>
      </span>

      <span className="absolute bottom-3 left-3 rounded-full bg-surface/95 px-3 py-1 text-sm font-medium text-ink shadow-card">
        Reproducir
      </span>
    </button>
  );
}
