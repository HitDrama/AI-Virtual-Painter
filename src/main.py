"""
AI Virtual Painter - Main Application
Vẽ tranh bằng ngón tay sử dụng webcam, MediaPipe và OpenCV

Controls:
- 1 finger (index): Draw mode
- 2 fingers (index + middle): Selection mode
- Press 'q': Quit
- Press 'c': Clear canvas
"""
import cv2
from hand_detector import HandDetector
from canvas import Canvas
from ui import UI


def main():
    print("Starting AI Virtual Painter...")
    print("Initializing webcam...")

    # Initialize webcam with DirectShow backend (Windows)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("ERROR: Cannot open webcam!")
        print("Please check:")
        print("  1. Webcam is connected")
        print("  2. No other app is using the webcam")
        print("  3. Try camera index 1: cv2.VideoCapture(1)")
        return

    print("Webcam opened successfully!")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Get actual dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if width == 0 or height == 0:
        print("ERROR: Invalid camera resolution!")
        return

    print(f"Camera resolution: {width}x{height}")
    print("\n=== AI Virtual Painter ===")
    print("Controls:")
    print("  - 1 finger (index): Draw")
    print("  - 2 fingers (index + middle): Select color/tool")
    print("  - Press 'c': Clear canvas")
    print("  - Press 'q': Quit")
    print("=" * 30)

    # Initialize components
    detector = HandDetector(max_hands=1, detection_confidence=0.7)
    canvas = Canvas(width, height)
    ui = UI(width, height, header_height=100)

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to read from camera")
            break

        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)

        # Detect hands
        frame = detector.find_hands(frame, draw=False)
        landmarks = detector.get_positions(frame)

        if landmarks:
            # Get finger states
            fingers = detector.fingers_up()
            x, y = detector.get_index_finger_tip()

            if x is not None:
                # Mode detection
                index_up = fingers[1]
                middle_up = fingers[2]

                if index_up and middle_up:
                    # Selection Mode - 2 fingers up
                    canvas.reset_previous_point()

                    # Check menu selection
                    result = ui.check_menu_selection(x, y)
                    if result == 'clear':
                        canvas.clear()

                    # Draw selection cursor
                    frame = ui.draw_cursor(frame, x, y, mode='select')
                    frame = ui.draw_mode_indicator(frame, 'select')

                elif index_up and not middle_up:
                    # Drawing Mode - only index finger up
                    # Don't draw in header area
                    if y > ui.header_height:
                        if ui.is_eraser:
                            canvas.erase(x, y, ui.current_thickness)
                        else:
                            canvas.draw_line(x, y, ui.current_color, ui.current_thickness)
                    else:
                        canvas.reset_previous_point()

                    # Draw drawing cursor
                    frame = ui.draw_cursor(frame, x, y, mode='draw')
                    frame = ui.draw_mode_indicator(frame, 'draw')
                else:
                    # No valid gesture - reset
                    canvas.reset_previous_point()
        else:
            # No hand detected - reset
            canvas.reset_previous_point()

        # Draw UI header
        frame = ui.draw_header(frame)

        # Blend canvas with frame
        frame = canvas.blend_with_frame(frame)

        # Show FPS
        cv2.putText(frame, f"Press 'q' to quit, 'c' to clear",
                   (width - 350, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Display
        cv2.imshow("AI Virtual Painter", frame)

        # Keyboard controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            canvas.clear()
            print("Canvas cleared!")

    cap.release()
    cv2.destroyAllWindows()
    print("\nGoodbye!")


if __name__ == "__main__":
    main()
