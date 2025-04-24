import os
import cv2
import numpy as np
from utils.disruption_chart import DisruptionChartOverlay
from utils.file_utils import get_video_rotation
from video_processing.mux_audio import mux_audio_back
from audio_processing.interpolate_disruption import interpolate

def process_video(video_path, disruption_timeline, effect_function, output_suffix, audio_path, accepts_threshold):
    output_folder = "outputs"  # If you want, can also load from config if needed

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    disruption_per_frame = interpolate(disruption_timeline, total_frames, fps)

    # 🌟 Detect rotation
    rotation = get_video_rotation(video_path)
    rotate_frames = rotation in [90, 270]

    # Read one frame to check orientation
    ret, test_frame = cap.read()
    if not ret:
        raise RuntimeError(f"Cannot read frames from {video_path}")

    if rotate_frames or test_frame.shape[1] > test_frame.shape[0]:
        rotate_frames = True
        width, height = height, width

    # Reset capture to beginning
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Create VideoWriter with correct dimensions
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    silent_output_name = os.path.basename(video_path).replace('.mp4', f'_{output_suffix}_silent.mp4')
    silent_output_path = os.path.join(output_folder, silent_output_name)
    out = cv2.VideoWriter(silent_output_path, fourcc, fps, (width, height))

    chart_overlay = DisruptionChartOverlay(disruption_timeline)
    dynamic_threshold = np.percentile(disruption_timeline, 75)

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if rotate_frames:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        disruption = disruption_per_frame[frame_idx]

        if accepts_threshold:
            frame = effect_function(frame, disruption, frame_idx, threshold=dynamic_threshold)
        else:
            frame = effect_function(frame, disruption, frame_idx)

        frame = chart_overlay.apply(frame, frame_idx, total_frames)

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()

    # 🎵 Mux original audio back
    final_output_name = os.path.basename(video_path).replace('.mp4', f'_{output_suffix}.mp4')
    final_output_path = os.path.join(output_folder, final_output_name)
    mux_audio_back(silent_output_path, audio_path, final_output_path)

    os.remove(silent_output_path)

    print(f"✅ Finished: {final_output_name}")
