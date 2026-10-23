// Renders an animation page frame by frame into an MP4 using Playwright + ffmpeg.
// PAGE selects the HTML (default moturi_promo.html); the page may set window.VIDEO_W / VIDEO_H.
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_PATH || 'playwright');
import { spawn } from 'child_process';
import path from 'path';
const FPS = 30, [,, out = 'moturi_promo_silent.mp4', only] = process.argv;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ viewport: { width: 1080, height: 1080 } });
await page.addInitScript(() => { window.__RENDERING__ = true; });
await page.goto('file://' + path.resolve(process.env.PAGE || 'moturi_promo.html'));
const size = await page.evaluate(() => [window.VIDEO_W || 1080, window.VIDEO_H || 1080]);
await page.setViewportSize({ width: size[0], height: size[1] });
await page.evaluate(() => document.fonts.ready);
const dur = await page.evaluate(() => window.DURATION);
if (only) { // snapshot mode: comma-separated seconds
  for (const s of only.split(',')) { await page.evaluate(t => render(t), +s); await page.screenshot({ path: `snap_${s}.png` }); }
  await browser.close(); process.exit(0);
}
const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], { stdio: ['pipe', 'ignore', 'inherit'] });
for (let f = 0; f < dur * FPS; f++) {
  await page.evaluate(t => render(t), f / FPS);
  const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
}
ff.stdin.end(); await new Promise(r => ff.on('close', r)); await browser.close();
