import { MEDITATIONS } from "@/data/meditations";
import { CHALLENGE } from "@/data/challenge";

const BASE_URL = "https://meditaciones.moturi.com";

export default function sitemap() {
  const staticRoutes = ["", "/meditaciones", "/desafio-10-dias"].map((path) => ({
    url: `${BASE_URL}${path}`,
  }));

  const meditationRoutes = MEDITATIONS.map((meditation) => ({
    url: `${BASE_URL}/meditaciones/${meditation.id}`,
  }));

  const challengeRoutes = CHALLENGE.map((day) => ({
    url: `${BASE_URL}/desafio-10-dias/${day.day}`,
  }));

  return [...staticRoutes, ...meditationRoutes, ...challengeRoutes];
}
