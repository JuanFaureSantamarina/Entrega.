"use client";

import { useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import FilterBar from "@/components/FilterBar";
import SearchBar from "@/components/SearchBar";
import MeditationCard from "@/components/MeditationCard";
import { MEDITATIONS } from "@/data/meditations";
import { filterMeditations } from "@/lib/filterMeditations";

export default function MeditationsExplorer() {
  const searchParams = useSearchParams();
  const initialCategory = searchParams.get("categoria");

  const [filters, setFilters] = useState({
    category: initialCategory || null,
    level: null,
    duration: null,
  });
  const [query, setQuery] = useState("");

  const results = useMemo(
    () => filterMeditations(MEDITATIONS, { ...filters, query }),
    [filters, query]
  );

  return (
    <section className="mx-auto max-w-content px-4 py-10 sm:px-6 sm:py-14">
      <div className="mb-8">
        <h1 className="font-display text-3xl font-semibold text-ink sm:text-4xl">
          Meditaciones
        </h1>
        <p className="mt-2 text-ink-soft">
          Explorá toda la biblioteca por categoría, nivel y duración.
        </p>
      </div>

      <div className="flex flex-col gap-4">
        <SearchBar value={query} onChange={setQuery} className="max-w-md" />
        <FilterBar
          filters={filters}
          onChange={(update) => setFilters((prev) => ({ ...prev, ...update }))}
          onReset={() => setFilters({ category: null, level: null, duration: null })}
        />
      </div>

      <p className="mt-6 text-sm text-muted" aria-live="polite">
        {results.length} {results.length === 1 ? "meditación encontrada" : "meditaciones encontradas"}
      </p>

      {results.length > 0 ? (
        <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {results.map((meditation) => (
            <MeditationCard key={meditation.id} meditation={meditation} />
          ))}
        </div>
      ) : (
        <div className="mt-10 rounded-xl2 border border-dashed border-line bg-surface p-8 text-center">
          <p className="font-medium text-ink">No encontramos meditaciones con esos filtros.</p>
          <p className="mt-1 text-sm text-ink-soft">Probá ajustar la búsqueda o limpiar los filtros.</p>
        </div>
      )}
    </section>
  );
}
