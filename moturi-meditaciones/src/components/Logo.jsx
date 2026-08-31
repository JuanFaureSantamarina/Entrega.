/**
 * Logo de MOTURI.
 *
 * Todavía no hay un archivo de logo oficial en el proyecto, así que por
 * ahora se muestra como texto estilizado (tal como pidió el brief).
 *
 * Para reemplazarlo por el logo real:
 * 1. Colocá el archivo en /public/logo.svg (preferido) o /public/logo.png.
 * 2. En este archivo, reemplazá el <span> de abajo por:
 *      <img src="/logo.svg" alt="MOTURI" className={...} />
 *    manteniendo las clases de tamaño que ya estén en uso.
 */
export default function Logo({ className = "" }) {
  return (
    <span
      className={`font-display text-xl font-semibold tracking-wide text-ink ${className}`}
    >
      MOTURI
    </span>
  );
}
