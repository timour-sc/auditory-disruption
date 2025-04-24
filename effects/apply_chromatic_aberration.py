import cv2
import numpy as np

def apply_chromatic_aberration(frame, disruption_strength, frame_idx, threshold=0.2):
    if disruption_strength < threshold:
        return frame  # Calm area: no chromatic split

    # Fade-in strength calculation
    fade_strength = (disruption_strength - threshold) / (1 - threshold)
    fade_strength = np.clip(fade_strength, 0, 1)

    shift_amount = int(fade_strength * 30)  # 🌟 Up to 30px shift at max disruption
    shift_amount = max(1, shift_amount)     # Minimum shift to see effect

    b, g, r = cv2.split(frame)

    # Shift each channel differently
    rows, cols = frame.shape[:2]
    M_b = np.float32([[1, 0, -shift_amount], [0, 1, 0]])
    M_r = np.float32([[1, 0, shift_amount], [0, 1, 0]])

    b_shifted = cv2.warpAffine(b, M_b, (cols, rows), borderMode=cv2.BORDER_REFLECT)
    r_shifted = cv2.warpAffine(r, M_r, (cols, rows), borderMode=cv2.BORDER_REFLECT)

    merged = cv2.merge((b_shifted, g, r_shifted))
    return merged
