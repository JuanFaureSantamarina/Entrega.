"use client";

import { useState } from "react";

const OPTIONS = ["Más tranquilo", "Igual", "Más activo", "Más enfocado", "Prefiero no responder"];

/**
 * Interacción opcional y no invasiva. No se guarda en ningún lado: es solo
 * un gesto de cierre para la persona que acaba de meditar.
 */
export default function MoodCheck() {
  const [selected, setSelected] = useState(null);

  return (
    <div className="rounded-xl2 border border-line bg-surface p-5">
      <h2 className="font-display text-base font-semibold text-ink">¿Cómo te sentís ahora?</h2>

      {selected ? (
        <p className="mt-3 text-sm text-ink-soft">Gracias por compartirlo. Que sigas bien.</p>
      ) : (
        <div className="mt-3 flex flex-wrap gap-2">
          {OPTIONS.map((option) => (
            <button
              key={option}
              type="button"
              onClick={() => setSelected(option)}
              className="rounded-full border border-line bg-paper px-3.5 py-1.5 text-sm text-ink-soft transition-colors hover:border-moturi/40 hover:text-ink focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi/40"
            >
              {option}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
