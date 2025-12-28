# AI Virtual Painter

Ứng dụng vẽ tranh bằng ngón tay sử dụng webcam, MediaPipe và OpenCV.

## Tính năng

- Nhận diện bàn tay real-time với MediaPipe
- Vẽ bằng ngón trỏ (Drawing Mode)
- Chọn màu và công cụ bằng 2 ngón (Selection Mode)
- Màu sắc: Đỏ, Xanh dương, Tím, Xanh lá
- Tẩy và xóa toàn bộ canvas
- Giao diện trực quan với menu header

## Cài đặt

### Yêu cầu
- Python 3.9+
- Webcam

### Bước cài đặt

```bash
# Clone hoặc download project
cd "AI Virtual Painter"

# Tạo virtual environment (khuyến nghị)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Cài đặt dependencies
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
cd src
python main.py
```

## Điều khiển

| Cử chỉ | Chức năng |
|--------|-----------|
| 1 ngón (trỏ) | Chế độ vẽ |
| 2 ngón (trỏ + giữa) | Chế độ chọn màu/công cụ |
| Phím 'c' | Xóa toàn bộ canvas |
| Phím 'q' | Thoát ứng dụng |

## Cấu trúc Project

```
AI Virtual Painter/
├── src/
│   ├── main.py           # Entry point
│   ├── hand_detector.py  # MediaPipe hand tracking
│   ├── canvas.py         # Drawing canvas layer
│   └── ui.py             # UI components
├── docs/
│   ├── design-guidelines.md
│   ├── tech-stack.md
│   └── system-architecture.md
├── assets/               # Resources (if needed)
├── requirements.txt
├── README.md
└── .gitignore
```

## Demo

```
┌─────────────────────────────────────────────────────────────┐
│  [RED] [BLUE] [PURPLE] [GREEN] [ERASER] [CLEAR]   ●        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    ✋ Vẽ tại đây                            │
│                                                             │
│                    🎨 Canvas Area                           │
│                                                             │
│  [DRAW]                              Press 'q' to quit     │
└─────────────────────────────────────────────────────────────┘
```

## Troubleshooting

| Vấn đề | Giải pháp |
|--------|-----------|
| Webcam không hoạt động | Kiểm tra camera ID trong `cv2.VideoCapture(0)` |
| Nét vẽ bị giật | Đảm bảo đủ ánh sáng, tay không bị che |
| Không nhận diện tay | Để tay trong tầm nhìn camera, đủ sáng |

## License

MIT License
