import { ImageResponse } from "next/og";

export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          background: "linear-gradient(135deg, #FAF8F4 0%, #DCE4EA 100%)",
          padding: 80,
        }}
      >
        <span
          style={{
            fontSize: 34,
            letterSpacing: 6,
            color: "#243B55",
            fontFamily: "Georgia, serif",
            fontWeight: 600,
          }}
        >
          MOTURI
        </span>
        <span
          style={{
            marginTop: 28,
            fontSize: 68,
            color: "#1D2430",
            fontFamily: "Georgia, serif",
            fontWeight: 600,
            textAlign: "center",
          }}
        >
          Meditaciones
        </span>
        <span
          style={{
            marginTop: 20,
            fontSize: 28,
            color: "#4B5563",
            textAlign: "center",
          }}
        >
          Un espacio para frenar, respirar y volver a vos.
        </span>
      </div>
    ),
    { ...size }
  );
}
