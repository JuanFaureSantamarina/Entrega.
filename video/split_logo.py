"""Splits the Moturi logo into white alpha masks: kettlebell, brain, leaf and full."""
import sys
import numpy as np
from PIL import Image
L = np.array(Image.open(sys.argv[1]).convert('L')).astype(float)
a = np.clip((235 - L) / (235 - 30), 0, 1)
H, W = a.shape
yy, xx = np.mgrid[:H, :W]
kb = ((xx < 318) | (yy < 218) | ((xx >= 376) & (yy < 254))) & (xx < 437)
leaf = (xx >= 437) & (yy < 250)
# fragments left over by the straight cuts are tiny islands: hand them to the leaf or the kettlebell
rest = (~kb) & ~leaf & (a > 0.3)
seen = np.zeros_like(rest)
for y0, x0 in zip(*np.where(rest)):
    if seen[y0, x0]:
        continue
    comp, stack = [], [(y0, x0)]
    seen[y0, x0] = True
    while stack:
        y, x = stack.pop()
        comp.append((y, x))
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < H and 0 <= nx < W and rest[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                stack.append((ny, nx))
    if len(comp) < 400:
        target = leaf if np.mean([x for _, x in comp]) >= 430 else kb
        for y, x in comp:
            target[max(0, y - 1):y + 2, max(0, x - 1):x + 2] = True
kb &= ~leaf
parts = {'kettlebell': kb, 'brain': (~kb) & ~leaf, 'leaf': leaf, 'full': np.ones_like(kb)}
cx, cy, s = (163 + 516) // 2, (127 + 507) // 2, 420
box = (cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2)
for name, m in parts.items():
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., :3] = 255
    rgba[..., 3] = (a * m * 255).astype(np.uint8)
    Image.fromarray(rgba).crop(box).resize((840, 840), Image.LANCZOS).save(f'assets/logo_{name}.png')

# colored variants used by the animation
for name in parts:
    im = Image.open(f'assets/logo_{name}.png')
    for cname, rgb in {'lime': (200, 241, 105), 'ink': (11, 31, 24)}.items():
        px = np.array(im)
        px[..., :3] = rgb
        Image.fromarray(px).save(f'assets/logo_{name}_{cname}.png')
