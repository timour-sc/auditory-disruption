import cv2
import numpy as np

def apply_radial_distortion(frame, disruption_strength, frame_idx):
    rows, cols, ch = frame.shape

    # Dynamic distortion level
    k = -0.0005 * disruption_strength * 10

    # Create normalized coordinate grid
    cx = cols / 2
    cy = rows / 2

    x = np.linspace(0, cols-1, cols)
    y = np.linspace(0, rows-1, rows)
    map_x, map_y = np.meshgrid(x, y)

    dx = (map_x - cx) / cx
    dy = (map_y - cy) / cy
    r2 = dx * dx + dy * dy

    map_x = map_x + (map_x - cx) * k * r2
    map_y = map_y + (map_y - cy) * k * r2

    map_x = map_x.astype(np.float32)
    map_y = map_y.astype(np.float32)

    distorted = cv2.remap(frame, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    return distorted
