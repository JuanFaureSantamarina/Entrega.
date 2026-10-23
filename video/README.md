# Video promocional de Moturi

`moturi_promo.mp4`: video animado de 42 s, 1080×1080, con voz de locutor y música original.

Guion: gancho → problema (estrés, burnout…) → "Hasta hoy." → aparece el logo completo dentro de un círculo lima y se llena de abajo hacia arriba → "Bienestar integral para personas y empresas" → recorrido por la app → para empresas → llamado a la acción.

## Archivos

- `moturi_promo.html`: la animación. Si lo abrís en el navegador, se reproduce en loop.
- `timeline.js`: en qué segundo entra cada frase del locutor. Las escenas y la música se acomodan solas a estos tiempos.
- `voiceover.py`: genera la voz (Kokoro TTS, voz `em_alex`). El guion completo está en `LINES`.
- `music.py` / `mix.py`: música sintetizada y mezcla final con la voz (la música baja sola cuando habla el locutor).
- `make_logo_assets.py`: genera el logo en blanco, lima y verde oscuro (`assets/`).

## Volver a generar

```bash
pip install kokoro-onnx soundfile
# modelos: https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0
mkdir -p build && (cd build && python3 ../voiceover.py kokoro-v1.0.onnx voices-v1.0.bin)
python3 music.py && python3 mix.py build
PLAYWRIGHT_PATH=$(npm root -g)/playwright node render.mjs build/silent.mp4
ffmpeg -y -i build/silent.mp4 -i soundtrack.wav -c:v copy -c:a aac -b:a 192k -shortest moturi_promo.mp4
```

Si cambiás una frase del guion, volvé a correr `voiceover.py`, mirá las duraciones en `build/vo_lines.json` y ajustá `timeline.js`.
