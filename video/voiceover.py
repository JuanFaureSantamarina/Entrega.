"""Generates the voice-over lines and writes their durations to vo_lines.json.

Usage:
  python3 voiceover.py piper <sherpa-onnx piper model dir> [speaker id] [speed]
  python3 voiceover.py kokoro <model.onnx> <voices.bin> [voice]
"""
import glob, json, sys
import numpy as np
import soundfile as sf

LINES = [
    ("hook",    "¿Cuándo fue la última vez... que te sentiste bien de verdad?"),
    ("pain",    "Estrés. Reuniones sin fin. Noches sin dormir."),
    ("pain2",   "La rutina te consume."),
    ("turn",    "Pero eso termina hoy."),
    ("brand",   "Esto es Moturi."),
    ("tag",     "Bienestar integral, para personas y empresas."),
    ("app1",    "Todo tu bienestar, en una sola app."),
    ("app2",    "Un plan que se adapta a vos, con hábitos que sí podés sostener."),
    ("app3",    "Y retos en equipo, porque el bienestar se contagia."),
    ("biz",     "Para empresas: programas a medida, y métricas reales de tu equipo."),
    ("biz2",    "Equipos más sanos. Equipos que rinden más."),
    ("cta",     "Con Moturi, empezá a sentirte bien hoy."),
]
# spelling tweaks so the synthesizer pronounces brand names right
SAY = {}

engine = sys.argv[1]
if engine == "piper":
    import sherpa_onnx
    d = sys.argv[2]
    sid = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    tts = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=glob.glob(f"{d}/*.onnx")[0], tokens=f"{d}/tokens.txt",
                                                   data_dir=f"{d}/espeak-ng-data"),
        num_threads=4)))
    def synth(text):
        a = tts.generate(text, sid=sid, speed=speed)
        return np.array(a.samples, dtype=np.float32), a.sample_rate
else:
    from kokoro_onnx import Kokoro
    k = Kokoro(sys.argv[2], sys.argv[3])
    voice = sys.argv[4] if len(sys.argv) > 4 else "em_alex"
    def synth(text):
        return k.create(text, voice=voice, speed=0.95, lang="es")

meta = {}
for key, text in LINES:
    for word, said in SAY.items():
        text = text.replace(word, said)
    samples, sr = synth(text)
    # trim leading/trailing silence so cues in timeline.js land on the first syllable
    idx = np.where(np.abs(samples) > 0.01)[0]
    if len(idx):
        samples = samples[max(0, idx[0] - int(.04 * sr)):idx[-1] + int(.3 * sr)]
    sf.write(f"vo_{key}.wav", samples, sr)
    meta[key] = round(len(samples) / sr, 3)
json.dump(meta, open("vo_lines.json", "w"), indent=1)
print(meta)
