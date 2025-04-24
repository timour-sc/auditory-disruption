import cv2
import numpy as np

def apply_shake(frame, disruption_strength, frame_idx):
    rows, cols, _ = frame.shape
    base_shift = 2
    dynamic_shift = base_shift + (disruption_strength ** 1.5) * 15  # Grow faster with chaos

    dx = int(np.sin(frame_idx / 3.0) * dynamic_shift)
    dy = int(np.cos(frame_idx / 5.0) * dynamic_shift)

    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(frame, M, (cols, rows))
