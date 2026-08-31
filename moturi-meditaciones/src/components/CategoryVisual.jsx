/**
 * Fondo visual decorativo por categoría (placeholder profesional).
 *
 * No usamos fotografía por ahora: cada categoría tiene un degradé propio
 * (dentro de la paleta de marca) más un trazo abstracto minimalista, en vez
 * de imágenes genéricas de "posición de loto". Es liviano (sin imágenes que
 * cargar) y fácil de reemplazar más adelante por fotografía real: alcanza
 * con editar este único archivo.
 *
 * Para reemplazar por una foto real en el futuro, agregá un <img> o
 * next/image dentro del `switch` de cada categoría, o agregá un campo
 * `image` en src/data/categories.js y usalo acá.
 */

const THEME = {
  calma: {
    gradient: "from-category-calma/20 via-category-calma/5 to-transparent",
    tint: "bg-category-calma/10",
  },
  enfoque: {
    gradient: "from-category-enfoque/20 via-category-enfoque/5 to-transparent",
    tint: "bg-category-enfoque/10",
  },
  sueno: {
    gradient: "from-category-sueno/25 via-category-sueno/5 to-transparent",
    tint: "bg-category-sueno/10",
  },
  presencia: {
    gradient: "from-category-presencia/20 via-category-presencia/5 to-transparent",
    tint: "bg-category-presencia/10",
  },
  autoconcepto: {
    gradient: "from-category-autoconcepto/20 via-category-autoconcepto/5 to-transparent",
    tint: "bg-category-autoconcepto/10",
  },
  emociones: {
    gradient: "from-category-emociones/20 via-category-emociones/5 to-transparent",
    tint: "bg-category-emociones/10",
  },
  energia: {
    gradient: "from-category-energia/20 via-category-energia/5 to-transparent",
    tint: "bg-category-energia/10",
  },
  gratitud: {
    gradient: "from-category-gratitud/20 via-category-gratitud/5 to-transparent",
    tint: "bg-category-gratitud/10",
  },
};

function CategoryMark({ slug, className }) {
  const common = { className, "aria-hidden": "true", viewBox: "0 0 64 64", fill: "none" };

  switch (slug) {
    case "calma":
      // ondas concéntricas
      return (
        <svg {...common}>
          <circle cx="32" cy="34" r="6" stroke="currentColor" strokeWidth="1.4" />
          <circle cx="32" cy="34" r="14" stroke="currentColor" strokeWidth="1.2" opacity="0.6" />
          <circle cx="32" cy="34" r="22" stroke="currentColor" strokeWidth="1" opacity="0.35" />
        </svg>
      );
    case "enfoque":
      // luz convergente
      return (
        <svg {...common}>
          <circle cx="32" cy="32" r="4" fill="currentColor" />
          <path d="M32 8v10M32 46v10M8 32h10M46 32h10" stroke="currentColor" strokeWidth="1.3" opacity="0.5" />
        </svg>
      );
    case "sueno":
      // luna
      return (
        <svg {...common}>
          <path
            d="M40 20a16 16 0 1 0 4 16 12 12 0 0 1-4-16Z"
            stroke="currentColor"
            strokeWidth="1.4"
          />
          <circle cx="20" cy="18" r="1.2" fill="currentColor" opacity="0.7" />
          <circle cx="14" cy="30" r="0.9" fill="currentColor" opacity="0.5" />
        </svg>
      );
    case "presencia":
      // hoja / forma orgánica
      return (
        <svg {...common}>
          <path
            d="M20 44C16 30 24 14 42 12c2 18-8 30-22 32Z"
            stroke="currentColor"
            strokeWidth="1.3"
          />
          <path d="M22 42C28 30 32 22 40 14" stroke="currentColor" strokeWidth="1" opacity="0.5" />
        </svg>
      );
    case "autoconcepto":
      // reflejo / horizonte
      return (
        <svg {...common}>
          <path d="M14 32h36" stroke="currentColor" strokeWidth="1.2" opacity="0.5" />
          <path d="M24 32V18l8-6 8 6v14" stroke="currentColor" strokeWidth="1.3" />
          <path d="M24 32v10l8 6 8-6V32" stroke="currentColor" strokeWidth="1.1" opacity="0.45" />
        </svg>
      );
    case "emociones":
      // capas de olas
      return (
        <svg {...common}>
          <path d="M10 26c6-4 10-4 16 0s10 4 16 0 10-4 12-2" stroke="currentColor" strokeWidth="1.3" />
          <path
            d="M10 36c6-4 10-4 16 0s10 4 16 0 10-4 12-2"
            stroke="currentColor"
            strokeWidth="1.1"
            opacity="0.5"
          />
        </svg>
      );
    case "energia":
      // amanecer
      return (
        <svg {...common}>
          <path d="M10 40h44" stroke="currentColor" strokeWidth="1.3" />
          <path d="M18 40a14 14 0 0 1 28 0" stroke="currentColor" strokeWidth="1.3" />
          <path d="M32 18v6M18 24l4 4M46 24l-4 4" stroke="currentColor" strokeWidth="1.1" opacity="0.6" />
        </svg>
      );
    case "gratitud":
      // arcos cálidos
      return (
        <svg {...common}>
          <path d="M12 40c8-14 32-14 40 0" stroke="currentColor" strokeWidth="1.3" />
          <path d="M18 40c6-9 22-9 28 0" stroke="currentColor" strokeWidth="1.1" opacity="0.55" />
          <circle cx="32" cy="22" r="2" fill="currentColor" opacity="0.7" />
        </svg>
      );
    default:
      return null;
  }
}

export default function CategoryVisual({ slug, size = "card", className = "" }) {
  const theme = THEME[slug] ?? THEME.calma;
  const iconSize = size === "hero" ? "h-16 w-16" : "h-10 w-10";

  return (
    <div
      className={`relative overflow-hidden bg-gradient-to-br ${theme.gradient} ${className}`}
    >
      <div className={`absolute inset-0 ${theme.tint}`} />
      <div className="absolute inset-0 flex items-center justify-center text-ink/70">
        <CategoryMark slug={slug} className={iconSize} />
      </div>
    </div>
  );
}
