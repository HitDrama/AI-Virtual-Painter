"""
Hand Detector Module - MediaPipe Hand Tracking
"""
import mediapipe as mp
import cv2


class HandDetector:
    """Detect hands and track finger positions using MediaPipe."""

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
