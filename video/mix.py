"""Mixes music.wav with the voice-over lines (placed per timeline.js) into soundtrack.wav.

Usage: python3 mix.py <dir with vo_*.wav>
"""
import json, re, subprocess, sys

vo_dir = sys.argv[1]
TL = json.loads(re.search(r'window\.TL\s*=\s*(\{.*\})', open('timeline.js').read(), re.S).group(1))
V = TL['vo']
inputs, chains = ['-i', 'music.wav'], []
for i, (key, start) in enumerate(V.items(), 1):
    inputs += ['-i', f'{vo_dir}/vo_{key}.wav']
    ms = int(start * 1000)
    chains.append(f'[{i}:a]aresample=44100,pan=stereo|c0=c0|c1=c0,adelay={ms}|{ms}[v{i}]')
n = len(V)
graph = ';'.join(chains) + ';' + ''.join(f'[v{i}]' for i in range(1, n + 1)) + \
    f'amix=inputs={n}:normalize=0,highpass=f=70,equalizer=f=220:t=q:w=1:g=2,equalizer=f=3000:t=q:w=1:g=3,aecho=0.9:0.6:28|47:0.10|0.06,' \
    'acompressor=threshold=0.1:ratio=3:attack=5:release=120,volume=1.6,' \
    f'apad=whole_dur={TL["duration"]},asplit=2[vo][key];' \
    '[0:a]volume=0.42[mus];[mus][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[duck];' \
    '[duck][vo]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', graph,
                '-map', '[out]', '-ar', '44100', 'soundtrack.wav'], check=True)
