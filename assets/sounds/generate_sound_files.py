# Small script to generate 100 different pitch files

import os

count = 64
print(f"Generating {count} different pitches")
# 0.1 - 1.0
for i in range(count):
    pitch_tone = -18 + i*0.5
    os.system(f"rubberband -t 0.2 -p {pitch_tone} harp.wav tone-{i}.wav")

