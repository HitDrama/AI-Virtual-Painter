"""
Hand Detector Module - MediaPipe Hand Tracking
21 Hand Landmarks Visualization for Educational Purpose
"""
import mediapipe as mp
import cv2


class HandDetector:
    """Detect hands and track finger positions using MediaPipe."""

    # 21 Hand Landmark Names (MediaPipe standard)
    LANDMARK_NAMES = [
        "WRIST",
        "THUMB_CMC", "THUMB_MCP", "THUMB_IP", "THUMB_TIP",
        "INDEX_MCP", "INDEX_PIP", "INDEX_DIP", "INDEX_TIP",
        "MIDDLE_MCP", "MIDDLE_PIP", "MIDDLE_DIP", "MIDDLE_TIP",
        "RING_MCP", "RING_PIP", "RING_DIP", "RING_TIP",
        "PINKY_MCP", "PINKY_PIP", "PINKY_DIP", "PINKY_TIP"
    ]

    # Color scheme for each finger (BGR format)
    FINGER_COLORS = {
        'wrist': (255, 255, 255),      # White
        'thumb': (0, 255, 255),         # Yellow
        'index': (0, 255, 0),           # Green
        'middle': (255, 0, 0),          # Blue
        'ring': (0, 165, 255),          # Orange
        'pinky': (255, 0, 255)          # Magenta
    }

    # Connections between landmarks for drawing skeleton
    HAND_CONNECTIONS = [
        # Thumb
        (0, 1), (1, 2), (2, 3), (3, 4),
        # Index
        (0, 5), (5, 6), (6, 7), (7, 8),
        # Middle
        (0, 9), (9, 10), (10, 11), (11, 12),
        # Ring
        (0, 13), (13, 14), (14, 15), (15, 16),
        # Pinky
        (0, 17), (17, 18), (18, 19), (19, 20),
        # Palm
        (5, 9), (9, 13), (13, 17)
    ]

    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
            model_complexity=0  # Lite model for performance
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        self.landmarks = []

    def find_hands(self, frame, draw=True):
        """Detect hands in frame and optionally draw landmarks."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
        return frame

    def get_positions(self, frame, hand_index=0):
        """Get landmark positions for specified hand."""
        self.landmarks = []
        if self.results.multi_hand_landmarks:
            if hand_index < len(self.results.multi_hand_landmarks):
                hand = self.results.multi_hand_landmarks[hand_index]
                h, w, _ = frame.shape
                for idx, lm in enumerate(hand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.landmarks.append((idx, cx, cy))
        return self.landmarks

    def get_finger_color(self, landmark_id):
        """Get color for a landmark based on which finger it belongs to."""
        if landmark_id == 0:
            return self.FINGER_COLORS['wrist']
        elif 1 <= landmark_id <= 4:
            return self.FINGER_COLORS['thumb']
        elif 5 <= landmark_id <= 8:
            return self.FINGER_COLORS['index']
        elif 9 <= landmark_id <= 12:
            return self.FINGER_COLORS['middle']
        elif 13 <= landmark_id <= 16:
            return self.FINGER_COLORS['ring']
        else:
            return self.FINGER_COLORS['pinky']

    def draw_hand_joints(self, frame, show_labels=True, show_ids=True):
        """
        Draw detailed hand joints visualization with labels.
        Educational/Academic visualization of 21 hand landmarks.
        """
        if not self.landmarks:
            return frame

        # Draw connections (skeleton)
        for connection in self.HAND_CONNECTIONS:
            start_idx, end_idx = connection
            if start_idx < len(self.landmarks) and end_idx < len(self.landmarks):
                start_point = (self.landmarks[start_idx][1], self.landmarks[start_idx][2])
                end_point = (self.landmarks[end_idx][1], self.landmarks[end_idx][2])
                color = self.get_finger_color(end_idx)
                cv2.line(frame, start_point, end_point, color, 2)

        # Draw landmarks with labels
        for idx, cx, cy in self.landmarks:
            color = self.get_finger_color(idx)

            # Draw outer circle (white border)
            cv2.circle(frame, (cx, cy), 8, (255, 255, 255), -1)
            # Draw inner circle (colored)
            cv2.circle(frame, (cx, cy), 6, color, -1)

            # Draw landmark ID
            if show_ids:
                cv2.putText(frame, str(idx), (cx - 5, cy + 4),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1)

            # Draw landmark name (for key points only to avoid clutter)
            if show_labels and idx in [0, 4, 8, 12, 16, 20]:  # Wrist and fingertips
                label = self.LANDMARK_NAMES[idx]
                # Background for text
                (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
                cv2.rectangle(frame, (cx + 10, cy - text_h - 5),
                             (cx + 15 + text_w, cy + 5), (0, 0, 0), -1)
                cv2.putText(frame, label, (cx + 12, cy),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

        return frame

    def draw_hand_info_panel(self, frame):
        """Draw an information panel showing hand landmark legend."""
        panel_x, panel_y = 10, 120
        panel_width, panel_height = 200, 180

        # Semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (panel_x, panel_y),
                     (panel_x + panel_width, panel_y + panel_height),
                     (30, 30, 30), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        # Title
        cv2.putText(frame, "HAND LANDMARKS", (panel_x + 10, panel_y + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.line(frame, (panel_x + 10, panel_y + 25),
                (panel_x + panel_width - 10, panel_y + 25), (100, 100, 100), 1)

        # Legend
        legend_items = [
            ("Wrist (0)", 'wrist'),
            ("Thumb (1-4)", 'thumb'),
            ("Index (5-8)", 'index'),
            ("Middle (9-12)", 'middle'),
            ("Ring (13-16)", 'ring'),
            ("Pinky (17-20)", 'pinky')
        ]

        for i, (text, color_key) in enumerate(legend_items):
            y_pos = panel_y + 45 + i * 22
            color = self.FINGER_COLORS[color_key]
            cv2.circle(frame, (panel_x + 20, y_pos), 6, color, -1)
            cv2.putText(frame, text, (panel_x + 35, y_pos + 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        return frame

    def fingers_up(self):
        """
        Check which fingers are raised.
        Returns list of 5 booleans [thumb, index, middle, ring, pinky].
        """
        fingers = []
        if not self.landmarks:
            return [False] * 5

        # Thumb - horizontal check (x comparison)
        if self.landmarks[self.tip_ids[0]][1] < self.landmarks[self.tip_ids[0] - 1][1]:
            fingers.append(True)
        else:
            fingers.append(False)

        # Other 4 fingers - vertical check (y comparison, smaller y = higher position)
        for i in range(1, 5):
            tip_y = self.landmarks[self.tip_ids[i]][2]
            pip_y = self.landmarks[self.tip_ids[i] - 2][2]
            fingers.append(tip_y < pip_y)

        return fingers

    def get_index_finger_tip(self):
        """Get position of index finger tip (landmark 8)."""
        if len(self.landmarks) > 8:
            return self.landmarks[8][1], self.landmarks[8][2]
        return None, None
