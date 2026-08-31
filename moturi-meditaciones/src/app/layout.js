import { Fraunces, Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const display = Fraunces({
  subsets: ["latin"],
  variable: "--font-display",
  weight: ["500", "600"],
  style: ["normal", "italic"],
  display: "swap",
});

const sans = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

export const metadata = {
  metadataBase: new URL("https://meditaciones.moturi.com"),
  title: {
    default: "Meditaciones | MOTURI",
    template: "%s | MOTURI",
  },
  description:
    "Meditaciones guiadas para ayudarte a bajar el ritmo, recuperar el foco, descansar y volver a vos.",
  openGraph: {
    title: "Meditaciones | MOTURI",
    description:
      "Meditaciones guiadas para ayudarte a bajar el ritmo, recuperar el foco, descansar y volver a vos.",
    siteName: "MOTURI",
    locale: "es_AR",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Meditaciones | MOTURI",
    description:
      "Meditaciones guiadas para ayudarte a bajar el ritmo, recuperar el foco, descansar y volver a vos.",
  },
};

export const viewport = {
  themeColor: "#FAF8F4",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }) {
  return (
    <html lang="es" className={`${display.variable} ${sans.variable}`}>
      <body className="flex min-h-screen flex-col font-sans antialiased">
        <a
          href="#contenido-principal"
          className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-full focus:bg-ink focus:px-4 focus:py-2 focus:text-sm focus:font-medium focus:text-surface"
        >
          Saltar al contenido principal
        </a>
        <Navbar />
        <main id="contenido-principal" className="flex-1">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
