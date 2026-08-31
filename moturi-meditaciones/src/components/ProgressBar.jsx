export default function ProgressBar({ value, total, className = "" }) {
  const percent = total > 0 ? Math.min(100, Math.round((value / total) * 100)) : 0;

  return (
    <div
      className={className}
      role="progressbar"
      aria-valuenow={value}
      aria-valuemin={0}
      aria-valuemax={total}
      aria-label={`${value} de ${total} días completados`}
    >
      <div className="h-2 w-full overflow-hidden rounded-full bg-mist">
        <div
          className="h-full rounded-full bg-sage transition-[width] duration-500 ease-calm"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
