"""Calm, confident corporate soundtrack for linkedin_promo.html -> linkedin_music.wav."""
import wave
import numpy as np

SR, DUR = 44100, 38.0
T = dict(s2=5.2, s3=10.0, s4=14.2, st1=18.4, st2=22.6, s5=27.0, s6=32.2)  # mirrors the HTML
out = np.zeros((int(SR * DUR), 2))
rng = np.random.default_rng(3)
n2f = lambda n: 440 * 2 ** ((n - 69) / 12)

def add(start, sig, pan=0.0, gain=1.0):
    i = int(start * SR); j = min(len(out), i + len(sig))
    if j > i:
        out[i:j, 0] += sig[:j - i] * gain * (1 - pan); out[i:j, 1] += sig[:j - i] * gain * (1 + pan)

def env(n, a, r):
    e = np.ones(n); a = int(a * SR); r = int(r * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e

def piano(m, start, dur=1.6, gain=.1, pan=0):
    n = int(dur * SR); tt = np.arange(n) / SR; f = n2f(m)
    s = sum(a * np.sin(2 * np.pi * f * h * tt) * np.exp(-tt * (2.5 + h)) for h, a in ((1, 1), (2, .45), (3, .2), (4, .08)))
    add(start, s * env(n, .004, .2), pan, gain)

def pad(notes, start, dur, gain=.04):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * n2f(m) * (1 + d) * tt) for m in notes for d in (-.0012, .0012))
    add(start, s * env(n, 1.0, 1.2) / len(notes), 0, gain)

def kick(start, gain=.3):
    n = int(.35 * SR); tt = np.arange(n) / SR
    add(start, np.sin(2 * np.pi * np.cumsum(48 + 80 * np.exp(-tt * 35)) / SR) * np.exp(-tt * 9), 0, gain)

def shaker(start, gain=.025, pan=.3):
    n = int(.08 * SR); s = np.diff(np.concatenate([[0], rng.standard_normal(n)]))
    add(start, s * np.sin(np.linspace(0, np.pi, n)) ** 2, pan, gain)

def swell(start, dur=1.0, gain=.06):
    n = int(dur * SR); s = np.convolve(rng.standard_normal(n), np.ones(40) / 40, 'same')
    add(start - dur, s * np.linspace(0, 1, n) ** 3, 0, gain)

BEAT = 60 / 96
chords = [[45, 52, 57, 60, 64], [41, 48, 53, 57, 60], [48, 55, 60, 64, 67], [43, 50, 55, 59, 62]]  # Am F C G
melody = [76, 72, 69, 72, 77, 72, 69, 72, 79, 76, 72, 76, 74, 71, 67, 71]
bar, s, ci = BEAT * 4, 0.0, 0
while s < T['s6']:
    ch = chords[ci % 4]
    pad(ch[1:], s, bar + 1.0, .05)
    piano(ch[0] - 12 + 12, s, 2.4, .09)
    for k in range(8):  # gentle eighth-note piano arpeggio
        tb = s + k * BEAT / 2
        if tb < T['s6']:
            piano(melody[(ci % 4) * 4 + k % 4] - (12 if k % 2 else 0), tb, 1.2, .045 if k % 2 else .06, (-.3, .3)[k % 2])
    if s >= T['s2'] - .05:
        for k in range(4):
            tb = s + k * BEAT
            if tb >= T['s6']: break
            kick(tb, .26 if k % 2 == 0 else .16)
            shaker(tb + BEAT / 2)
            if s >= T['s4']: shaker(tb + BEAT / 4, .015, -.3); shaker(tb + 3 * BEAT / 4, .015, -.3)
    s += bar; ci += 1
for key in ('s2', 's3', 's4', 's5', 's6'):
    swell(T[key], 1.0, .07)
# resolve on the CTA: wide C major with a slow arpeggio
pad([36, 48, 55, 60, 64, 67, 72], T['s6'], DUR - T['s6'], .07)
kick(T['s6'], .35)
for k, m in enumerate([60, 64, 67, 72, 76, 79]):
    piano(m, T['s6'] + .2 + k * .28, 3.0, .07, (k - 2.5) * .15)
for k, m in enumerate([72, 76, 79, 84]):
    piano(m, T['s6'] + 3.0 + k * .5, 2.5, .04)

fade = int(2.0 * SR)
out[-fade:] *= np.linspace(1, 0, fade)[:, None]
out /= np.abs(out).max() / .85
with wave.open('linkedin_music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
