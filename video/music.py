"""Synthesizes an original soundtrack synced to the Moturi promo scenes."""
import numpy as np, wave
SR, DUR = 44100, 32.0
t = np.arange(int(SR*DUR))/SR
out = np.zeros((len(t), 2))
n2f = lambda n: 440*2**((n-69)/12)

def env(n, a, r):
    e = np.ones(n); a=int(a*SR); r=int(r*SR)
    if a: e[:a] = np.linspace(0,1,a)
    if r: e[-r:] *= np.linspace(1,0,r)
    return e

def add(start, sig, pan=0.0, gain=1.0):
    i = int(start*SR); j = min(len(t), i+len(sig)); sig = sig[:j-i]*gain
    out[i:j,0] += sig*(1-pan)/1.0; out[i:j,1] += sig*(1+pan)/1.0

def pad(notes, start, dur, gain=.05):
    n = int(dur*SR); tt = np.arange(n)/SR; s = np.zeros(n)
    for m in notes:
        f = n2f(m)
        for d in (-0.08, 0.08):
            s += np.sin(2*np.pi*f*(1+d/100)*tt) + .25*np.sin(4*np.pi*f*tt)
    add(start, s*env(n, .6, .8), 0, gain/len(notes))

def pluck(m, start, dur=.5, gain=.12, pan=0):
    n=int(dur*SR); tt=np.arange(n)/SR; f=n2f(m)
    s=(np.sin(2*np.pi*f*tt)+.4*np.sin(4*np.pi*f*tt)+.15*np.sin(6*np.pi*f*tt))*np.exp(-tt*7)
    add(start, s*env(n,.003,.05), pan, gain)

def kick(start, gain=.5):
    n=int(.35*SR); tt=np.arange(n)/SR; f=50+90*np.exp(-tt*30)
    add(start, np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*9), 0, gain)

def hat(start, gain=.04, pan=.3):
    n=int(.06*SR); s=np.random.randn(n); s=np.diff(np.concatenate([[0],s]))
    add(start, s*np.exp(-np.arange(n)/SR*60), pan, gain)

def swell(start, dur, gain=.12, rev=False):
    n=int(dur*SR); s=np.random.randn(n)
    s=np.convolve(s, np.ones(30)/30, 'same'); e=np.linspace(0,1,n)**2
    add(start, s*(e[::-1] if rev else e), 0, gain)

def impact(start, gain=.6):
    kick(start, gain); n=int(1.5*SR); s=np.convolve(np.random.randn(n),np.ones(8)/8,'same')
    add(start, s*np.exp(-np.arange(n)/SR*3), 0, .15)

np.random.seed(7)
BEAT = 60/96
# Hook: dark drone + heartbeat
pad([45, 52], 0, 4.6, .07)
for b in np.arange(0.4, 4.2, BEAT*2): kick(b, .25); kick(b+.18, .15)
# Pain: tension, clock ticks, riser
pad([44, 51, 56], 4.2, 4.6, .07)
for i,b in enumerate(np.arange(4.2, 8.4, BEAT/2)): hat(b, .03+.04*i/14, .5 if i%2 else -.5)
swell(5.8, 2.8, .18)
# Brand reveal
impact(8.62)
for k,m in enumerate([72,76,79,84]): pluck(m, 9.3+k*.12, 1.2, .1, (k-1.5)*.3)
# Main groove 9.4 → 27
chords = [[53,57,60,64],[55,59,62,67],[57,60,64,67],[48,52,55,59]]  # Fmaj7 G Am7 Cmaj7
bar = BEAT*4
s = 9.4; ci = 0
while s < 27.2:
    ch = chords[ci%4]; pad(ch, s, bar+.6, .06)
    add(s, np.sin(2*np.pi*n2f(ch[0]-12)*np.arange(int(bar*SR))/SR)*env(int(bar*SR),.02,.3), 0, .09)
    for k in range(8):
        pluck(ch[k%4]+12 + (12 if k in (3,7) else 0), s+k*BEAT/2, .45, .07, (-.4,.4)[k%2])
    for k in range(4):
        if s > 12.4: kick(s+k*BEAT, .35)
        hat(s+k*BEAT+BEAT/2, .035)
    s += bar; ci += 1
swell(21.2, .8, .08); swell(26.4, .9, .1)
# CTA: resolve
impact(27.25, .45)
pad([48,55,60,64,67], 27.3, 4.7, .08)
for k,m in enumerate([72,76,79,83,84]): pluck(m, 28.3+k*.15, 1.5, .09, (k-2)*.25)
for k,m in enumerate([79, 84]): pluck(m, 29.05+k*.1, 1.5, .1)

out[-int(1.2*SR):] *= np.linspace(1,0,int(1.2*SR))[:,None]
out /= np.abs(out).max()/0.85
with wave.open('music.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out*32767).astype(np.int16).tobytes())
