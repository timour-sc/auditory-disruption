import cv2
import numpy as np

def apply_fast_moving_ripple(frame, disruption_strength, frame_idx):
    rows, cols, ch = frame.shape

    map_x, map_y = np.meshgrid(np.arange(cols), np.arange(rows))

    ripple_magnitude = 5 + disruption_strength * 30
    base_frequency = 50
    dynamic_frequency = base_frequency - disruption_strength * 20
    dynamic_frequency = max(dynamic_frequency, 10)  # Safety cap

    # 🔥 New: frame_idx * disruption_strength = dynamic phase shift
    phase_shift = (frame_idx * disruption_strength * 2 * np.pi) / dynamic_frequency

    displacement = ripple_magnitude * np.sin((2 * np.pi * map_y / dynamic_frequency) + phase_shift)

    map_x = (map_x + displacement).astype(np.float32)
    map_y = map_y.astype(np.float32)

    ripple_frame = cv2.remap(frame, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    return ripple_frame
