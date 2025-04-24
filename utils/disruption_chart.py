import matplotlib
matplotlib.use('Agg')  # <-- ADD THIS
import matplotlib.pyplot as plt
import cv2
import numpy as np

class DisruptionChartOverlay:
    def __init__(self, disruption_timeline, width=400, height=100, position=(10, 10)):
        self.disruption_timeline = disruption_timeline
        self.width = width
        self.height = height
        self.position = position  # (x_offset, y_offset)
        self.base_chart = self._generate_base_chart()

    def _generate_base_chart(self):
        fig, ax = plt.subplots(figsize=(self.width/100, self.height/100), dpi=100)
        ax.plot(self.disruption_timeline, color='purple')
        ax.set_axis_off()
        plt.tight_layout(pad=0)
        fig.canvas.draw()

    # ✅ Corrected way to extract image
        renderer = fig.canvas.get_renderer()
        img = np.frombuffer(renderer.buffer_rgba(), dtype=np.uint8)
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (4,))
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

        plt.close(fig)
        return img


    def _draw_marker(self, frame_idx, total_frames):
        overlay = self.base_chart.copy()
        height, width, _ = overlay.shape

        x = int((frame_idx / total_frames) * width)
        cv2.line(overlay, (x, 0), (x, height), (0, 0, 255), 2)  # Red vertical line

        return overlay

    def apply(self, frame, frame_idx, total_frames):
        chart_with_marker = self._draw_marker(frame_idx, total_frames)
        return self._overlay_on_frame(frame, chart_with_marker)

    def _overlay_on_frame(self, frame, chart_img):
        ch, cw, _ = chart_img.shape
        x_offset, y_offset = self.position

        # Ensure it doesn't overflow frame
        if y_offset + ch > frame.shape[0] or x_offset + cw > frame.shape[1]:
            return frame  # Skip overlay if chart too big

        frame[y_offset:y_offset+ch, x_offset:x_offset+cw] = chart_img
        return frame
