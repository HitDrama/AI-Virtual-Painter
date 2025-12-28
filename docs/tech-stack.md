# AI Virtual Painter - Tech Stack

## Core Technologies

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Language | Python | 3.9+ | Main programming language |
| Computer Vision | OpenCV | 4.8+ | Webcam capture, image processing, drawing |
| Hand Tracking | MediaPipe | 0.10+ | Real-time hand detection & landmarks |
| Array Processing | NumPy | 1.24+ | Efficient array operations |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Main Application                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │   Webcam    │→ │  MediaPipe  │→ │  Hand Detector  │ │
│  │   Input     │  │   Hands     │  │   (21 points)   │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
│                                            ↓            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │   Display   │← │   Canvas    │← │ Finger Counter  │ │
│  │   Output    │  │   Layer     │  │  (Drawing Mode) │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Why This Stack?

1. **MediaPipe Hands**: Pre-trained ML model, 21 landmarks, real-time performance
2. **OpenCV**: Industry standard for computer vision, excellent Python bindings
3. **NumPy**: Fast array operations for canvas manipulation
4. **Python**: Rapid development, extensive ML ecosystem

## Performance

- Target: 30+ FPS on standard webcam
- MediaPipe runs inference on CPU efficiently (model_complexity=0)
- Canvas operations use NumPy bitwise ops for speed
- Minimal memory footprint (~100MB)
