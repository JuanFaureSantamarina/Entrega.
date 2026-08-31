import Link from "next/link";
import CategoryVisual from "./CategoryVisual";

export default function CategoryCard({ category }) {
  return (
    <Link
      href={`/meditaciones?categoria=${category.slug}`}
      className="group flex flex-col overflow-hidden rounded-xl2 border border-line bg-surface shadow-card transition-all duration-300 ease-calm hover:-translate-y-1 hover:shadow-soft focus-visible:-translate-y-1 focus-visible:shadow-soft focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-moturi/40"
    >
      <CategoryVisual slug={category.slug} className="aspect-[4/3] w-full" />
      <div className="flex flex-1 flex-col gap-1 p-4">
        <h3 className="font-display text-lg font-semibold text-ink">{category.name}</h3>
        <p className="text-sm leading-relaxed text-ink-soft">{category.objective}</p>
      </div>
    </Link>
  );
}
