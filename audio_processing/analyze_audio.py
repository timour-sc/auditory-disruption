import librosa
import numpy as np
import os
import json
from utils.audio_utils import normalize

with open('config.json') as f:
    config = json.load(f)

def analyze_audio(audio_path):
    y, sr = librosa.load(audio_path, sr=config['sample_rate'])
    window_size = int(sr / config['measurements_per_second'])

    flatness = []
    variability = []

    for i in range(0, len(y), window_size):
        chunk = y[i:i+window_size]
        if len(chunk) == 0:
            continue
        flatness.append(np.mean(librosa.feature.spectral_flatness(y=chunk)))
        variability.append(np.std(chunk))

    flatness_norm = normalize(flatness)
    variability_norm = normalize(variability)

    disruption = (0.6 * flatness_norm) + (0.4 * variability_norm)
    return disruption
