"""
Canvas Module - Drawing layer management
"""
import numpy as np
import cv2


class Canvas:
    """Manage the drawing canvas layer."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.xp, self.yp = 0, 0  # Previous point

    def draw_line(self, x, y, color, thickness):
        """Draw a line from previous point to current point."""
        if self.xp == 0 and self.yp == 0:
            self.xp, self.yp = x, y

        cv2.line(self.canvas, (self.xp, self.yp), (x, y), color, thickness)
        self.xp, self.yp = x, y

    def erase(self, x, y, thickness=50):
        """Erase by drawing black."""
        if self.xp == 0 and self.yp == 0:
            self.xp, self.yp = x, y

        cv2.line(self.canvas, (self.xp, self.yp), (x, y), (0, 0, 0), thickness)
        self.xp, self.yp = x, y

    def reset_previous_point(self):
        """Reset previous point to avoid connecting lines."""
        self.xp, self.yp = 0, 0

    def clear(self):
        """Clear the entire canvas."""
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.reset_previous_point()

    def blend_with_frame(self, frame):
        """
        Blend canvas with video frame using bitwise operations.
        More performant than addWeighted.
        """
        # Convert canvas to grayscale for mask
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, inv_mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY_INV)
        inv_mask = cv2.cvtColor(inv_mask, cv2.COLOR_GRAY2BGR)

        # Create holes in frame where drawing exists
        frame_masked = cv2.bitwise_and(frame, inv_mask)

        # Combine frame with canvas
        result = cv2.bitwise_or(frame_masked, self.canvas)

        return result
