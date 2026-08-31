import Link from "next/link";

export default function NotFound() {
  return (
    <section className="mx-auto flex max-w-content flex-col items-center px-4 py-24 text-center sm:px-6">
      <h1 className="font-display text-3xl font-semibold text-ink">No encontramos esta página</h1>
      <p className="mt-3 max-w-sm text-ink-soft">
        Puede que el link haya cambiado. Volvé a la biblioteca de meditaciones.
      </p>
      <Link
        href="/meditaciones"
        className="mt-6 inline-flex items-center justify-center rounded-full bg-moturi px-6 py-3 text-sm font-semibold text-surface transition-transform hover:scale-[1.02] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi/40"
      >
        Ir a Meditaciones
      </Link>
    </section>
  );
}
