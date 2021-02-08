# Small script to generate 100 different pitch files

import os

count = 64
print(f"Generating {count} different pitches")
# 0.1 - 1.0
"""for i in range(count):
    pitch_tone = -8 + i*0.4
    os.system(f"rubberband -t 0.1 -p {pitch_tone} tone.wav tone-{i}.wav") """

for i in range(count):
    pitch_tone = -16 + i*0.7
    os.system(f"rubberband -t 0.5 -p {pitch_tone} harp.wav tone-{i}.wav")

