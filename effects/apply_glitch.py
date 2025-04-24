import numpy as np
import cv2

def apply_glitch(frame, disruption_strength, frame_idx, threshold=0.2):
    if disruption_strength < threshold:
        return frame  # Calm area: no glitch

    # Fade in effect: 0 at threshold, 1 at max disruption
    fade_strength = (disruption_strength - threshold) / (1 - threshold)
    fade_strength = np.clip(fade_strength, 0, 1)

    height, width, _ = frame.shape
    max_glitch_intensity = 20  # Maximum number of glitch lines per frame
    glitch_intensity = int(fade_strength * max_glitch_intensity)

    for _ in range(glitch_intensity):
        y1 = np.random.randint(0, height)
        y2 = np.clip(y1 + np.random.randint(5, 12), 0, height)  # Thin stripe
        x_shift = np.random.randint(-10, 10)

        frame[y1:y2, :] = np.roll(frame[y1:y2, :], x_shift, axis=1)

    return frame
