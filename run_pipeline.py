import os
import json
from concurrent.futures import ProcessPoolExecutor

from audio_processing.extract_audio import extract_audio
from audio_processing.analyze_audio import analyze_audio
from utils.file_utils import ensure_folder_exists
from video_processing.process_video import process_video
from effects.apply_blur import apply_blur
from effects.apply_fast_moving_ripple import apply_fast_moving_ripple
from effects.apply_glitch import apply_glitch
from effects.apply_shake import apply_shake
from effects.apply_chromatic_aberration import apply_chromatic_aberration
from effects.apply_overexposure_pulses import apply_overexposure_pulses
from effects.apply_radial_distortion import apply_radial_distortion
from effects.apply_combined_effect import apply_combined_effect

import inspect

# Load config
with open('config.json') as f:
    config = json.load(f)

# Effect registry
EFFECT_REGISTRY = {
    "blur": apply_blur,
    "ripple": apply_fast_moving_ripple,
    "glitch": apply_glitch,
    "shake": apply_shake,
    "chromatic": apply_chromatic_aberration,
    "pulse": apply_overexposure_pulses,
    "radial": apply_radial_distortion,
    "glitch_pulse": lambda frame, disruption, frame_idx, threshold=0.2: apply_combined_effect(
        frame, disruption, frame_idx, effects=[apply_glitch, apply_overexposure_pulses], threshold=threshold
    ),
    "glitch_chromatic": lambda frame, disruption, frame_idx, threshold=0.2: apply_combined_effect(
        frame, disruption, frame_idx, effects=[apply_glitch, apply_chromatic_aberration], threshold=threshold
    )
}

def process_single_video(video_filename, effects_to_run):
    video_folder = config['video_folder']
    audio_folder = config['audio_folder']
    video_path = os.path.join(video_folder, video_filename)
    audio_filename = video_filename.replace('.mp4', '.wav')
    audio_path = os.path.join(audio_folder, audio_filename)

    print(f"\n▶️ Processing video: {video_filename}")

    print("Extracting audio...")
    extract_audio(video_path, audio_path)

    print("Analyzing audio disruption...")
    disruption_timeline = analyze_audio(audio_path)

    print("Applying selected visual effects...")

    for effect_name in effects_to_run:
        if effect_name in EFFECT_REGISTRY:
            print(f"  ➡️ Applying effect: {effect_name}")
            effect_function = EFFECT_REGISTRY[effect_name]
            accepts_threshold = len(inspect.signature(effect_function).parameters) == 4

            process_video(video_path, disruption_timeline, effect_function, effect_name, audio_path, accepts_threshold)
        else:
            print(f"⚠️ Warning: Effect '{effect_name}' is not recognized!")

def main():
    video_folder = config['video_folder']
    effects_to_run = config.get('effects_to_run', ["blur", "ripple", "glitch", "shake"])

    ensure_folder_exists(config['audio_folder'])
    ensure_folder_exists(config['output_folder'])

    mp4_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
    if not mp4_files:
        print("No .mp4 files found.")
        return

    max_workers = min(4, os.cpu_count() or 1)
    print(f"\n🚀 Starting parallel processing with {max_workers} workers...")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for video_filename in mp4_files:
            futures.append(executor.submit(process_single_video, video_filename, effects_to_run))

        for future in futures:
            future.result()  # Wait for all to complete

    print("\n✅ All videos processed successfully!")

if __name__ == "__main__":
    main()
