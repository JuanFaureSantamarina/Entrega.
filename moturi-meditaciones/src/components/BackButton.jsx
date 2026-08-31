"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

/**
 * Botón de volver. Por defecto usa el historial del navegador; si se pasa
 * `href`, navega directamente ahí (útil cuando se llega por link directo o
 * QR y no hay historial previo dentro del sitio).
 */
export default function BackButton({ href, label = "Volver", className = "" }) {
  const router = useRouter();

  const content = (
    <>
      <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" aria-hidden="true">
        <path d="M12 4 6 10l6 6" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      {label}
    </>
  );

  const classes = `inline-flex items-center gap-1.5 rounded-full bg-surface px-4 py-2 text-sm font-medium text-ink-soft shadow-card transition-colors hover:text-ink focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi/40 ${className}`;

  if (href) {
    return (
      <Link href={href} className={classes}>
        {content}
      </Link>
    );
  }

  return (
    <button type="button" onClick={() => router.back()} className={classes}>
      {content}
    </button>
  );
}
