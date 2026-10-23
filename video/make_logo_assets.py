"""Turns the Moturi logo into transparent PNGs (white, lime and ink) used by the animation."""
import sys
import numpy as np
from PIL import Image

L = np.array(Image.open(sys.argv[1]).convert('L')).astype(float)
alpha = (np.clip((235 - L) / (235 - 30), 0, 1) * 255).astype(np.uint8)
cx, cy, s = (163 + 516) // 2, (127 + 507) // 2, 420
box = (cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2)
for suffix, rgb in {'': (255, 255, 255), '_lime': (200, 241, 105), '_ink': (11, 31, 24)}.items():
    rgba = np.zeros(L.shape + (4,), np.uint8)
    rgba[..., :3] = rgb
    rgba[..., 3] = alpha
    Image.fromarray(rgba).crop(box).resize((840, 840), Image.LANCZOS).save(f'assets/logo_full{suffix}.png')
