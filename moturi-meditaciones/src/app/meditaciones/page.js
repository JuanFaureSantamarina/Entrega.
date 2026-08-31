import { Suspense } from "react";
import MeditationsExplorer from "./MeditationsExplorer";

export const metadata = {
  title: "Meditaciones",
  description: "Explorá toda la biblioteca de meditaciones de MOTURI por categoría, nivel y duración.",
};

export default function MeditationsPage() {
  return (
    <Suspense fallback={null}>
      <MeditationsExplorer />
    </Suspense>
  );
}
