export default function SearchBar({ value, onChange, className = "" }) {
  return (
    <div className={`relative ${className}`}>
      <svg
        viewBox="0 0 20 20"
        className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted"
        fill="none"
        stroke="currentColor"
        aria-hidden="true"
      >
        <circle cx="8.5" cy="8.5" r="5.5" strokeWidth="1.5" />
        <path d="m17 17-4-4" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
      <input
        type="search"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Buscar meditación…"
        aria-label="Buscar meditación por nombre"
        className="w-full rounded-full border border-line bg-surface py-2.5 pl-10 pr-4 text-sm text-ink placeholder:text-muted focus:border-moturi/50 focus:outline-none focus:ring-2 focus:ring-moturi/30"
      />
    </div>
  );
}
