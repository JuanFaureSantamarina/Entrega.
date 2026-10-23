# Video promocional de Moturi

`moturi_promo.mp4`: video animado de 42 s, 1080×1080, con voz de locutor y música original.

Guion: gancho → problema (estrés, burnout…) → "Termina hoy." → aparece el logo completo dentro de un círculo lima y se llena de abajo hacia arriba → "Bienestar integral para personas y empresas" → recorrido por la app → para empresas → llamado a la acción.

## Archivos

- `moturi_promo.html`: la animación. Si lo abrís en el navegador, se reproduce en loop.
- `timeline.js`: en qué segundo entra cada frase del locutor. Las escenas y la música se acomodan solas a estos tiempos.
- `voiceover.py`: genera la voz del locutor (voz neuronal Piper `es_MX-claude-high`, vía sherpa-onnx). El guion completo está en `LINES`.
- `music.py` / `mix.py`: música sintetizada y mezcla final con la voz (la música baja sola cuando habla el locutor).
- `make_logo_assets.py`: genera el logo en blanco, lima y verde oscuro (`assets/`).

## Volver a generar

```bash
pip install sherpa-onnx soundfile
curl -LO https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-es_MX-claude-high.tar.bz2
tar xjf vits-piper-es_MX-claude-high.tar.bz2
mkdir -p build && (cd build && python3 ../voiceover.py piper ../vits-piper-es_MX-claude-high)
python3 music.py && python3 mix.py build
PLAYWRIGHT_PATH=$(npm root -g)/playwright node render.mjs build/silent.mp4
ffmpeg -y -i build/silent.mp4 -i soundtrack.wav -c:v copy -c:a aac -b:a 192k -shortest moturi_promo.mp4
```

Si cambiás una frase del guion, volvé a correr `voiceover.py`, mirá las duraciones en `build/vo_lines.json` y ajustá `timeline.js`.

---

# Versión LinkedIn (sin voz)

`moturi_linkedin.mp4`: 38 s, vertical 4:5 (1080×1350), estética editorial y formal, solo música de fondo; el mensaje se entiende sin sonido.

Guion: dato de la OMS (12 mil millones de días de trabajo perdidos por depresión y ansiedad) → "El bienestar de tu equipo no es un beneficio. Es una estrategia." → marca → cómo trabajamos (01 Diagnóstico, 02 Programas a medida, 03 Seguimiento con IA) → personas y empresas → "Agendá una reunión".

```bash
python3 music_linkedin.py
PAGE=linkedin_promo.html PLAYWRIGHT_PATH=$(npm root -g)/playwright node render.mjs build/li_silent.mp4
ffmpeg -y -i build/li_silent.mp4 -i linkedin_music.wav -af loudnorm=I=-16:TP=-1.5 -c:v copy -c:a aac -b:a 192k -shortest moturi_linkedin.mp4
```
