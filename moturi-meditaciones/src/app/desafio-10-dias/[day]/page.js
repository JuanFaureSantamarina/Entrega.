import { notFound } from "next/navigation";
import ChallengeDayView from "./ChallengeDayView";
import { CHALLENGE, getChallengeDay } from "@/data/challenge";
import { getMeditationById } from "@/data/meditations";

export function generateStaticParams() {
  return CHALLENGE.map((item) => ({ day: String(item.day) }));
}

export function generateMetadata({ params }) {
  const day = getChallengeDay(params.day);
  if (!day) return {};

  return {
    title: `Día ${day.day} · Desafío de 10 días`,
    description: day.objective,
  };
}

export default function ChallengeDayPage({ params }) {
  const day = getChallengeDay(params.day);
  if (!day) notFound();

  const meditation = getMeditationById(day.meditationId);
  if (!meditation) notFound();

  return <ChallengeDayView day={day} meditation={meditation} />;
}
