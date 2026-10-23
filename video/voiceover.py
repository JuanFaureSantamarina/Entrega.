"""Generates the voice-over lines with Kokoro TTS and writes their durations to vo_lines.json.

Usage: python3 voiceover.py <model.onnx> <voices.bin> [voice]
"""
import json, sys
import soundfile as sf
from kokoro_onnx import Kokoro

LINES = [
    ("hook",    "¿Cuándo fue la última vez... que te sentiste bien de verdad?"),
    ("pain",    "Estrés. Reuniones sin fin. Noches sin dormir."),
    ("pain2",   "La rutina te consume."),
    ("turn",    "Hasta hoy."),
    ("brand",   "Esto es Moturi."),
    ("tag",     "Bienestar integral, para personas y empresas."),
    ("app1",    "Todo tu bienestar, en una sola app."),
    ("app2",    "Un plan que se adapta a vos, con hábitos que sí podés sostener."),
    ("app3",    "Y retos en equipo, porque el bienestar se contagia."),
    ("biz",     "Para empresas: programas a medida y métricas reales de tu equipo."),
    ("biz2",    "Equipos más sanos. Equipos que rinden más."),
    ("cta",     "Moturi. Empezá a sentirte bien."),
]

k = Kokoro(sys.argv[1], sys.argv[2])
voice = sys.argv[3] if len(sys.argv) > 3 else "em_alex"
meta = {}
for key, text in LINES:
    samples, sr = k.create(text, voice=voice, speed=0.95, lang="es")
    sf.write(f"vo_{key}.wav", samples, sr)
    meta[key] = round(len(samples) / sr, 3)
json.dump(meta, open("vo_lines.json", "w"), indent=1)
print(meta)
