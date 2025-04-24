import cv2

def apply_blur(frame, disruption_strength, frame_idx):
    if disruption_strength == 0:
        return frame

    # Make blur strength grow exponentially at high disruption
    blur_factor = 1 + (disruption_strength ** 2) * 40  # Square to boost effect
    ksize = int(blur_factor)
    ksize = ksize if ksize % 2 == 1 else ksize + 1

    return cv2.GaussianBlur(frame, (ksize, ksize), 0)
