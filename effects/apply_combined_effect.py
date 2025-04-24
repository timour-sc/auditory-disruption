def apply_combined_effect(frame, disruption_strength, frame_idx, effects=[], threshold=0.2):
    """
    Apply multiple effects sequentially to the same frame.

    Parameters:
    - frame: current video frame (numpy array)
    - disruption_strength: float between 0 and 1
    - frame_idx: current frame index
    - effects: list of functions [effect1, effect2, ...] to apply
    """
    combined_frame = frame.copy()

    for effect in effects:
        combined_frame = effect(combined_frame, disruption_strength, frame_idx)

    return combined_frame
