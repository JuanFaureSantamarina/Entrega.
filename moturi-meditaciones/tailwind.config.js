/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // Paleta MOTURI: blancos suaves, grises claros, azules profundos, arena.
        paper: "#FAF8F4", // fondo general, blanco cálido
        surface: "#FFFFFF", // tarjetas y superficies
        mist: "#F1EEE7", // superficie secundaria / hover sutil
        line: "#E4DFD5", // bordes suaves
        ink: "#1D2430", // texto principal, azul-carbón profundo
        "ink-soft": "#4B5563", // texto secundario
        muted: "#8B8779", // texto terciario / metadatos
        moturi: {
          DEFAULT: "#243B55", // azul profundo, color de marca
          deep: "#152436",
          soft: "#5C7A99", // azul desaturado
          mist: "#DCE4EA", // azul muy suave, fondos
        },
        sand: {
          DEFAULT: "#EFE6D8",
          deep: "#D9C9AE",
        },
        warm: "#C08457", // detalle cálido, usar con moderación
        sage: "#6E8271", // acentos naturales / progreso
        category: {
          calma: "#3E5C76",
          enfoque: "#4A5568",
          sueno: "#22304A",
          presencia: "#5C7160",
          autoconcepto: "#6B5B6E",
          emociones: "#8A6A6A",
          energia: "#AD7A3D",
          gratitud: "#B08463",
        },
      },
      fontFamily: {
        display: ["var(--font-display)", "Georgia", "serif"],
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
      },
      borderRadius: {
        xl2: "1.25rem",
      },
      boxShadow: {
        soft: "0 8px 30px -12px rgba(29, 36, 48, 0.15)",
        card: "0 2px 14px -4px rgba(29, 36, 48, 0.10)",
      },
      maxWidth: {
        content: "72rem",
      },
      transitionTimingFunction: {
        calm: "cubic-bezier(0.4, 0, 0.2, 1)",
      },
    },
  },
  plugins: [],
};
