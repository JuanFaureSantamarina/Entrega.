import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-line/70 bg-paper">
      <div className="mx-auto flex max-w-content flex-col items-center gap-3 px-4 py-10 text-center sm:px-6">
        <span className="font-display text-lg font-semibold text-ink">MOTURI</span>
        <p className="text-sm text-ink-soft">Bienestar para todos los días.</p>
        <nav aria-label="Navegación del pie de página">
          <ul className="mt-2 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm text-ink-soft">
            <li>
              <Link href="/" className="transition-colors hover:text-ink">
                Inicio
              </Link>
            </li>
            <li>
              <Link href="/meditaciones" className="transition-colors hover:text-ink">
                Meditaciones
              </Link>
            </li>
            <li>
              <Link href="/desafio-10-dias" className="transition-colors hover:text-ink">
                Desafío de 10 días
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </footer>
  );
}
