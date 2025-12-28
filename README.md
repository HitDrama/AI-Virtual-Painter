# AI Virtual Painter

Ứng dụng vẽ tranh bằng ngón tay sử dụng webcam, MediaPipe và OpenCV.

## Mục lục

- [Tính năng](#tính-năng)
- [Thuật toán & Công thức](#thuật-toán--công-thức)
- [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Điều khiển](#điều-khiển)
- [Cấu trúc Project](#cấu-trúc-project)

---

## Tính năng

- Nhận diện bàn tay real-time với MediaPipe (21 landmarks)
- Vẽ bằng ngón trỏ (Drawing Mode)
- Chọn màu và công cụ bằng 2 ngón (Selection Mode)
- Hiển thị Hand Joints với color-coding theo ngón tay
- Màu sắc: Đỏ, Xanh dương, Tím, Xanh lá
- Tẩy và xóa toàn bộ canvas
- Giao diện trực quan với menu header

---

## Thuật toán & Công thức

### 1. Hand Landmark Detection (MediaPipe)

MediaPipe sử dụng **Machine Learning pipeline** với 2 model:

```
Input Frame → Palm Detector → Hand Landmark Model → 21 3D Landmarks
```

**Palm Detector**: Single Shot Detector (SSD) để tìm vùng bàn tay
**Hand Landmark Model**: Regression model dự đoán 21 điểm landmarks

#### 21 Hand Landmarks

```
              4 (THUMB_TIP)
              │
         8    3    12        16        20
         │    │    │         │         │    ← Fingertips (TIP)
         7    2    11        15        19
         │    │    │         │         │    ← DIP joints
         6    1    10        14        18
         │    │    │         │         │    ← PIP joints
         5────────9─────────13────────17    ← MCP joints (knuckles)
                   \         │        /
                    \        │       /
                     ────────0───────       ← WRIST
```

### 2. Finger Detection Algorithm

#### Công thức phát hiện ngón tay giơ lên

**Với 4 ngón (Index, Middle, Ring, Pinky):**

So sánh tọa độ Y của đầu ngón (TIP) với khớp PIP:

```python
finger_up = (TIP.y < PIP.y)
```

> **Lưu ý**: Trong OpenCV, trục Y hướng xuống dưới, nên `y nhỏ hơn = vị trí cao hơn`

| Ngón tay | TIP ID | PIP ID | Công thức |
|----------|--------|--------|-----------|
| Index | 8 | 6 | `landmarks[8].y < landmarks[6].y` |
| Middle | 12 | 10 | `landmarks[12].y < landmarks[10].y` |
| Ring | 16 | 14 | `landmarks[16].y < landmarks[14].y` |
| Pinky | 20 | 18 | `landmarks[20].y < landmarks[18].y` |

**Với ngón cái (Thumb):**

So sánh tọa độ X (vì ngón cái di chuyển ngang):

```python
thumb_up = (THUMB_TIP.x < THUMB_IP.x)  # Tay phải
thumb_up = (THUMB_TIP.x > THUMB_IP.x)  # Tay trái
```

#### Code Implementation

```python
def fingers_up(self):
    fingers = []

    # Thumb - horizontal check
    if landmarks[4].x < landmarks[3].x:
        fingers.append(True)
    else:
        fingers.append(False)

    # Other 4 fingers - vertical check
    tip_ids = [8, 12, 16, 20]
    for tip_id in tip_ids:
        if landmarks[tip_id].y < landmarks[tip_id - 2].y:
            fingers.append(True)
        else:
            fingers.append(False)

    return fingers  # [thumb, index, middle, ring, pinky]
```

### 3. Gesture Recognition

#### Selection Mode vs Drawing Mode

```python
# Lấy trạng thái ngón tay
fingers = detector.fingers_up()
index_up = fingers[1]   # Ngón trỏ
middle_up = fingers[2]  # Ngón giữa

# Logic phân biệt mode
if index_up and middle_up:
    mode = "SELECTION"  # 2 ngón = chọn màu/công cụ
elif index_up and not middle_up:
    mode = "DRAWING"    # 1 ngón = vẽ
else:
    mode = "IDLE"       # Không làm gì
```

### 4. Coordinate Transformation

#### Chuyển đổi từ Normalized → Pixel coordinates

MediaPipe trả về tọa độ normalized `[0.0, 1.0]`:

```python
# Normalized coordinates từ MediaPipe
x_norm = landmark.x  # 0.0 → 1.0
y_norm = landmark.y  # 0.0 → 1.0

# Chuyển sang pixel coordinates
x_pixel = int(x_norm * frame_width)
y_pixel = int(y_norm * frame_height)
```

### 5. Drawing Algorithm

#### Smooth Line Drawing

Để vẽ nét mượt, cần nối điểm trước đó với điểm hiện tại:

```python
# Lưu điểm trước đó
xp, yp = previous_point

# Điểm hiện tại
x1, y1 = current_point

# Vẽ đường nối
cv2.line(canvas, (xp, yp), (x1, y1), color, thickness)

# Cập nhật điểm trước đó
xp, yp = x1, y1
```

#### Reset Logic

Khi tay ra khỏi khung hình hoặc đổi mode, reset điểm trước đó để tránh vẽ đường thẳng lạ:

```python
if hand_not_detected or mode_changed:
    xp, yp = 0, 0  # Reset
```

### 6. Canvas Blending Algorithm

#### Bitwise Operations (Hiệu suất cao)

```python
def blend_with_frame(self, frame):
    # 1. Chuyển canvas sang grayscale
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

    # 2. Tạo mask ngược (vùng có vẽ = đen, vùng trống = trắng)
    _, inv_mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY_INV)
    inv_mask = cv2.cvtColor(inv_mask, cv2.COLOR_GRAY2BGR)

    # 3. Tạo "lỗ" trên frame tại vị trí có vẽ
    frame_masked = cv2.bitwise_and(frame, inv_mask)

    # 4. Gộp frame đã tạo lỗ với canvas
    result = cv2.bitwise_or(frame_masked, canvas)

    return result
```

**Giải thích visual:**

```
Frame (Webcam)     Canvas (Drawing)    inv_mask           Result
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  ┌────────┐  │   │              │   │  ████████████│   │  ┌────────┐  │
│  │ Person │  │ + │    ~~~       │ → │  ███    █████│ = │  │ Person │  │
│  └────────┘  │   │   /   \      │   │  ████████████│   │  └───~~~──┘  │
│              │   │              │   │              │   │     /   \    │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

### 7. Menu Selection Algorithm

#### Region of Interest (ROI) Check

```python
def check_menu_selection(x, y):
    # Kiểm tra có trong vùng header không
    if y > header_height:
        return False

    # Xác định item nào được chọn
    item_width = screen_width / num_items
    selected_index = x // item_width

    return menu_items[selected_index]
```

---

## Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MAIN LOOP (30 FPS)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌──────────────────┐    ┌──────────────────┐  │
│  │   WEBCAM    │ →  │   MEDIAPIPE      │ →  │  HAND DETECTOR   │  │
│  │   INPUT     │    │   PROCESSING     │    │  (21 landmarks)  │  │
│  │             │    │                  │    │                  │  │
│  │ cv2.Video   │    │ RGB conversion   │    │ Finger counting  │  │
│  │ Capture()   │    │ Hand detection   │    │ Gesture recog.   │  │
│  └─────────────┘    └──────────────────┘    └──────────────────┘  │
│                                                      │              │
│                              ┌───────────────────────┘              │
│                              ↓                                      │
│  ┌─────────────┐    ┌──────────────────┐    ┌──────────────────┐  │
│  │   DISPLAY   │ ←  │     CANVAS       │ ←  │   MODE LOGIC     │  │
│  │   OUTPUT    │    │     LAYER        │    │                  │  │
│  │             │    │                  │    │ DRAW / SELECT    │  │
│  │ cv2.imshow  │    │ Bitwise blend    │    │ Color/Tool pick  │  │
│  │             │    │ with frame       │    │                  │  │
│  └─────────────┘    └──────────────────┘    └──────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. Webcam capture frame (BGR, 1280x720)
       ↓
2. Flip horizontally (mirror effect)
       ↓
3. Convert BGR → RGB (for MediaPipe)
       ↓
4. MediaPipe detect 21 landmarks
       ↓
5. Convert normalized → pixel coordinates
       ↓
6. Count fingers up [T, I, M, R, P]
       ↓
7. Determine mode (DRAW/SELECT/IDLE)
       ↓
8. If DRAW: cv2.line() on canvas
   If SELECT: check menu ROI
       ↓
9. Blend canvas with frame (bitwise ops)
       ↓
10. Draw UI overlay (header, cursor)
       ↓
11. Display result with cv2.imshow()
```

---

## Cài đặt

### Yêu cầu
- Python 3.9+
- Webcam
- Windows/Linux/MacOS

### Bước cài đặt

```bash
# Clone repository
git clone https://github.com/HitDrama/AI-Virtual-Painter.git
cd AI-Virtual-Painter

# Tạo virtual environment (khuyến nghị)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Cài đặt dependencies
pip install -r requirements.txt
```

### Chạy ứng dụng

```bash
cd src
python main.py
```

---

## Điều khiển

### Cử chỉ tay

| Cử chỉ | Chức năng |
|--------|-----------|
| ☝️ 1 ngón (trỏ) | Chế độ vẽ |
| ✌️ 2 ngón (trỏ + giữa) | Chế độ chọn màu/công cụ |

### Phím tắt

| Phím | Chức năng |
|------|-----------|
| `h` | Bật/tắt hiển thị Hand Joints |
| `l` | Bật/tắt landmark labels |
| `c` | Xóa toàn bộ canvas |
| `q` | Thoát ứng dụng |

---

## Cấu trúc Project

```
AI Virtual Painter/
├── src/
│   ├── main.py           # Entry point, main loop
│   ├── hand_detector.py  # MediaPipe hand tracking, finger detection
│   ├── canvas.py         # Drawing canvas, blending algorithms
│   └── ui.py             # UI components, menu system
├── docs/
│   ├── hand-landmarks.md     # 21 landmarks documentation
│   ├── design-guidelines.md  # UI/UX design specs
│   ├── tech-stack.md         # Technology overview
│   └── system-architecture.md
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Demo

```
┌─────────────────────────────────────────────────────────────────┐
│  [RED] [BLUE] [PURPLE] [GREEN] [ERASER] [CLEAR]   ●  JOINTS:ON │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────────┐                                                │
│ │HAND LANDMARKS│      ✋ ← Hand with 21 joints displayed        │
│ │ ○ Wrist (0)  │           Color-coded by finger                │
│ │ ○ Thumb (1-4)│                                                │
│ │ ○ Index (5-8)│                                                │
│ │ ...          │      🎨 Canvas Area                            │
│ └──────────────┘                                                │
│  [DRAW]                    h: joints | l: labels | c: clear    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

| Vấn đề | Giải pháp |
|--------|-----------|
| Webcam không hoạt động | Thử `cv2.VideoCapture(1)` thay vì `0` |
| Nét vẽ bị giật | Đảm bảo đủ ánh sáng, tay không bị che |
| Không nhận diện tay | Để tay trong tầm nhìn camera, background đơn giản |
| TensorFlow warning | Không ảnh hưởng, có thể bỏ qua |

---

## Tham khảo

- [MediaPipe Hands Documentation](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)
- [OpenCV Drawing Functions](https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html)
- [Hand Anatomy Reference](https://en.wikipedia.org/wiki/Hand)

---

## License

MIT License

## Author

Created with ❤️ using MediaPipe, OpenCV, and Python.
