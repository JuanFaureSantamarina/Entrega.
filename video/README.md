# Video promocional de Moturi

`moturi_promo.mp4`: video animado de 32 s, 1080×1080, con música original sintetizada.

Guion: gancho → dolor (estrés, burnout…) → aparece la marca → recorrido por la app → para empresas → llamado a la acción.

## Editar y volver a generar

Los textos, los colores y los tiempos están en `moturi_promo.html`. Si lo abrís en el navegador, se reproduce en loop.

```bash
python3 music.py                               # genera music.wav
PLAYWRIGHT_PATH=$(npm root -g)/playwright node render.mjs moturi_promo_silent.mp4
ffmpeg -i moturi_promo_silent.mp4 -i music.wav -c:v copy -c:a aac -shortest moturi_promo.mp4
```
