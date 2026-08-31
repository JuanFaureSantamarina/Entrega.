/**
 * Helpers para trabajar con URLs de YouTube (o placeholders sin reemplazar).
 */

const PLACEHOLDER_PREFIX = "YOUTUBE_URL_REEMPLAZAR";

export function isPlaceholderUrl(url) {
  return !url || url.startsWith(PLACEHOLDER_PREFIX);
}

/**
 * Extrae el ID de un video a partir de distintos formatos de URL de YouTube.
 * Devuelve null si la URL no es válida o todavía es un placeholder.
 */
export function getYoutubeVideoId(url) {
  if (isPlaceholderUrl(url)) return null;

  try {
    const parsed = new URL(url);

    if (parsed.hostname === "youtu.be") {
      return parsed.pathname.slice(1) || null;
    }

    if (parsed.hostname.includes("youtube.com")) {
      if (parsed.pathname === "/watch") {
        return parsed.searchParams.get("v");
      }
      if (parsed.pathname.startsWith("/embed/")) {
        return parsed.pathname.split("/embed/")[1] || null;
      }
      if (parsed.pathname.startsWith("/shorts/")) {
        return parsed.pathname.split("/shorts/")[1] || null;
      }
    }

    return null;
  } catch {
    return null;
  }
}

export function getYoutubeThumbnailUrl(url) {
  const id = getYoutubeVideoId(url);
  if (!id) return null;
  return `https://i.ytimg.com/vi/${id}/hqdefault.jpg`;
}

export function getYoutubeEmbedUrl(url) {
  const id = getYoutubeVideoId(url);
  if (!id) return null;
  return `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0&modestbranding=1`;
}
