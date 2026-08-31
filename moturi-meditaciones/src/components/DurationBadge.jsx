import { formatDuration } from "@/lib/format";

export default function DurationBadge({ minutes, className = "" }) {
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full bg-mist px-2.5 py-1 text-xs font-medium text-ink-soft ${className}`}
    >
      <svg
        aria-hidden="true"
        viewBox="0 0 20 20"
        className="h-3.5 w-3.5"
        fill="none"
        stroke="currentColor"
      >
        <circle cx="10" cy="10" r="7.5" strokeWidth="1.4" />
        <path d="M10 6v4l3 2" strokeWidth="1.4" strokeLinecap="round" />
      </svg>
      {formatDuration(minutes)}
    </span>
  );
}
