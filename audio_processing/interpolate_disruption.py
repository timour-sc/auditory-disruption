import numpy as np

def interpolate(timeline, total_frames, fps):
    disruption_per_frame = []
    for frame in range(total_frames):
        second = frame / fps
        lower = int(np.floor(second))
        upper = int(np.ceil(second))
        if lower == upper:
            disruption = timeline[min(lower, len(timeline)-1)]
        else:
            low_val = timeline[min(lower, len(timeline)-1)]
            up_val = timeline[min(upper, len(timeline)-1)]
            alpha = (second - lower)
            disruption = (1 - alpha) * low_val + alpha * up_val
        disruption_per_frame.append(disruption)
    return disruption_per_frame
