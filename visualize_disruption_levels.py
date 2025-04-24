import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import json

from utils.audio_utils import normalize

# Load config
with open('config.json') as f:
    config = json.load(f)

def analyze_audio(audio_path):
    """Simple reimplementation of disruption analysis for visualization"""
    y, sr = librosa.load(audio_path, sr=config['sample_rate'])
    window_size = int(sr / config['measurements_per_second'])

    flatness = []
    variability = []
    rms_energy = []

    for i in range(0, len(y), window_size):
        chunk = y[i:i+window_size]
        if len(chunk) == 0:
            continue
        flatness.append(np.mean(librosa.feature.spectral_flatness(y=chunk)))
        variability.append(np.std(chunk))
        rms_energy.append(np.sqrt(np.mean(chunk**2)))

    flatness_norm = normalize(flatness)
    variability_norm = normalize(variability)
    rms_norm = normalize(rms_energy)

    disruption = (0.6 * flatness_norm) + (0.4 * variability_norm)

    return flatness_norm, variability_norm, rms_norm, disruption

def main():
    video_folder = config['video_folder']
    audio_folder = config['audio_folder']

    mp4_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
    if not mp4_files:
        print("No .mp4 files found.")
        return

    video_filename = mp4_files[0]
    audio_path = os.path.join(audio_folder, video_filename.replace('.mp4', '.wav'))

    if not os.path.exists(audio_path):
        print(f"Audio file {audio_path} not found. Please extract audio first.")
        return

    flatness, variability, rms_energy, disruption = analyze_audio(audio_path)

    # Plotting
    x = np.linspace(0, len(flatness) / config['measurements_per_second'], len(flatness))

    plt.figure(figsize=(12, 8))

    plt.subplot(4, 1, 1)
    plt.plot(x, flatness, label='Spectral Flatness', color='red')
    plt.title('Spectral Flatness Over Time')
    plt.ylabel('Normalized Flatness')
    plt.grid(True)

    plt.subplot(4, 1, 2)
    plt.plot(x, variability, label='Amplitude Variability', color='blue')
    plt.title('Amplitude Variability Over Time')
    plt.ylabel('Normalized Variability')
    plt.grid(True)

    plt.subplot(4, 1, 3)
    plt.plot(x, rms_energy, label='RMS Energy', color='green')
    plt.title('RMS Energy Over Time')
    plt.ylabel('Normalized RMS Energy')
    plt.grid(True)

    plt.subplot(4, 1, 4)
    plt.plot(x, disruption, label='Composite Disruption', color='purple')
    plt.title('Composite Audio Disruption Level Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Disruption Index')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
