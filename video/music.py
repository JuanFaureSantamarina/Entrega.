"""Synthesizes an original soundtrack synced to the scenes in timeline.js -> music.wav."""
import json, re, wave
import numpy as np

TL = json.loads(re.search(r'window\.TL\s*=\s*(\{.*\})', open('timeline.js').read(), re.S).group(1))
V, DUR = TL['vo'], TL['duration']
# scene boundaries, mirrored from moturi_promo.html
S = dict(s2=4.3, turn=V['turn'] - .15, s3=V['turn'] + .85, s3b=V['body'] - .4,
         s4=V['app1'] - .5, s5=V['biz'] - .4, s6=V['cta'] - .7)

SR = 44100
out = np.zeros((int(SR * DUR), 2))
n2f = lambda n: 440 * 2 ** ((n - 69) / 12)
rng = np.random.default_rng(7)

def env(n, a, r):
    e = np.ones(n); a = int(a * SR); r = int(r * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e

def add(start, sig, pan=0.0, gain=1.0):
    i = int(start * SR); j = min(len(out), i + len(sig))
    if j <= i: return
    sig = sig[:j - i] * gain
    out[i:j, 0] += sig * (1 - pan); out[i:j, 1] += sig * (1 + pan)

def pad(notes, start, dur, gain=.05, bright=.25):
    n = int(dur * SR); tt = np.arange(n) / SR; s = np.zeros(n)
    for m in notes:
        f = n2f(m)
        for d in (-0.1, 0.1):
            s += np.sin(2 * np.pi * f * (1 + d / 100) * tt) + bright * np.sin(4 * np.pi * f * tt)
    add(start, s * env(n, .5, .8), 0, gain / len(notes))

def pluck(m, start, dur=.5, gain=.1, pan=0):
    n = int(dur * SR); tt = np.arange(n) / SR; f = n2f(m)
    s = (np.sin(2 * np.pi * f * tt) + .4 * np.sin(4 * np.pi * f * tt) + .15 * np.sin(6 * np.pi * f * tt)) * np.exp(-tt * 7)
    add(start, s * env(n, .003, .05), pan, gain)

def kick(start, gain=.5, low=50):
    n = int(.4 * SR); tt = np.arange(n) / SR; f = low + 100 * np.exp(-tt * 30)
    add(start, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 8), 0, gain)

def noise(n):
    return rng.standard_normal(n)

def hat(start, gain=.04, pan=.3):
    n = int(.06 * SR); s = np.diff(np.concatenate([[0], noise(n)]))
    add(start, s * np.exp(-np.arange(n) / SR * 60), pan, gain)

def clap(start, gain=.12):
    n = int(.25 * SR); s = np.convolve(noise(n), [1, -1], 'same')
    add(start, s * np.exp(-np.arange(n) / SR * 18), 0, gain)

def riser(start, dur, gain=.15):
    n = int(dur * SR); s = np.convolve(noise(n), np.ones(12) / 12, 'same')
    tt = np.arange(n) / SR; tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (tt / dur) ** 2) / SR)
    add(start, (s + .3 * tone) * (tt / dur) ** 2.5, 0, gain)

def whoosh(start, dur=.6, gain=.12):
    n = int(dur * SR); s = np.convolve(noise(n), np.ones(20) / 20, 'same')
    e = np.sin(np.linspace(0, np.pi, n)) ** 2
    add(start - dur / 2, s * e, 0, gain)

def impact(start, gain=.7):
    kick(start, gain, 40)
    n = int(2.0 * SR); s = np.convolve(noise(n), np.ones(6) / 6, 'same')
    add(start, s * np.exp(-np.arange(n) / SR * 2.5), 0, .12)
    sub = np.sin(2 * np.pi * 36 * np.arange(n) / SR) * np.exp(-np.arange(n) / SR * 1.5)
    add(start, sub, 0, .35)

# 1. Hook: dark drone + heartbeat synced to the pulsing glow (period 1.25 s)
pad([38, 45, 52], 0, S['s2'] + .4, .08, .1)
for b in np.arange(.3125 - .06, S['s2'], 1.25):
    kick(b, .32, 45); kick(b + .2, .2, 45)

# 2. Pain: rising tension, clock ticks, glitch hit, then silence before "Hasta hoy."
pad([37, 44, 49], S['s2'], S['turn'] - S['s2'] - .3, .09, .4)
for i, b in enumerate(np.arange(S['s2'], S['turn'] - .45, .3125)):
    hat(b, .03 + .05 * min(1, i / 14), .5 if i % 2 else -.5)
    if i % 2 == 0: kick(b, .18, 55)
impact(V['pain2'], .45)
riser(V['pain2'] + .3, S['turn'] - V['pain2'] - .6, .16)

# 3. Brand reveal: impact on the flash, hit when the logo locks, sparkle arpeggio
impact(S['s3'], .8)
whoosh(S['s3'] + .3, .7, .1)
impact(S['s3'] + 1.0, .5)
for k, m in enumerate([72, 76, 79, 84, 88]):
    pluck(m, S['s3'] + 1.0 + k * .09, 1.4, .09, (k - 2) * .25)
pad([48, 55, 60, 64], S['s3'], S['s3b'] - S['s3'] + .3, .07, .3)

# 4. Main groove (100 bpm) from body/mind until the CTA
BEAT = 60 / 100
bar = BEAT * 4
chords = [[53, 57, 60, 64], [55, 59, 62, 67], [57, 60, 64, 67], [48, 52, 55, 59]]  # Fmaj7 G Am7 Cmaj7
s, ci = S['s3b'], 0
while s < S['s6'] - .05:
    ch = chords[ci % 4]
    blen = min(bar, S['s6'] - s)
    pad(ch, s, blen + .6, .06)
    nb = int(blen * SR)
    add(s, np.sin(2 * np.pi * n2f(ch[0] - 12) * np.arange(nb) / SR) * env(nb, .02, .2), 0, .1)
    for k in range(8):
        if s + k * BEAT / 2 < S['s6'] - .1:
            pluck(ch[k % 4] + 12 + (12 if k in (3, 7) else 0), s + k * BEAT / 2, .45, .06, (-.4, .4)[k % 2])
    for k in range(4):
        tb = s + k * BEAT
        if tb >= S['s6'] - .1: break
        kick(tb, .38)
        hat(tb + BEAT / 2, .035)
        if k % 2 == 1 and s >= S['s4']: clap(tb, .08)
    s += bar; ci += 1
for key in ('s4', 's5'):
    whoosh(S[key], .7, .12)
riser(S['s6'] - 1.6, 1.5, .12)

# 5. CTA: big resolve and outro
impact(S['s6'], .7)
pad([36, 48, 55, 60, 64, 67], S['s6'], DUR - S['s6'], .1, .3)
for k, m in enumerate([72, 76, 79, 83, 84]):
    pluck(m, S['s6'] + .3 + k * .15, 1.6, .08, (k - 2) * .25)
for k in range(6):
    pluck([84, 88, 91][k % 3], V['cta'] + 1.5 + k * .3, 1.2, .05, (k % 2 - .5) * .6)

fade = int(1.5 * SR)
out[-fade:] *= np.linspace(1, 0, fade)[:, None]
out /= np.abs(out).max() / 0.85
with wave.open('music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
