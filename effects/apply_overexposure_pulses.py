import cv2
import numpy as np

def apply_overexposure_pulses(frame, disruption_strength, frame_idx):
    frame = frame.astype(np.float32) / 255.0  # Normalize to 0-1

    # Pulse brightness randomly at higher disruption
    pulse_chance = 0.05 + disruption_strength * 0.4  # Chance grows with disruption

    if np.random.rand() < pulse_chance:
        pulse_intensity = 1.0 + disruption_strength * np.random.uniform(0.5, 1.5)
        if np.random.rand() < 0.5:
            frame = frame * pulse_intensity  # Overexpose
        else:
            frame = frame * (1.0 / pulse_intensity)  # Underexpose

    frame = np.clip(frame, 0, 1)
    frame = (frame * 255).astype(np.uint8)

    return frame
