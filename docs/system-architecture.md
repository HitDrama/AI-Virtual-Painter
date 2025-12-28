# AI Virtual Painter - System Architecture

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      MAIN LOOP                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    Input Layer                          │ │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────────────┐   │ │
│  │  │ Webcam   │ → │  Flip    │ → │   Frame Buffer   │   │ │
│  │  │ Capture  │   │ (Mirror) │   │                  │   │ │
│  │  └──────────┘   └──────────┘   └──────────────────┘   │ │
│  └────────────────────────────────────────────────────────┘ │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  Processing Layer                       │ │
│  │  ┌──────────────┐   ┌──────────────┐                   │ │
│  │  │ HandDetector │ → │ Finger State │                   │ │
│  │  │ (MediaPipe)  │   │   Counter    │                   │ │
│  │  └──────────────┘   └──────────────┘                   │ │
│  │          ↓                  ↓                           │ │
│  │  ┌──────────────┐   ┌──────────────┐                   │ │
│  │  │  21 Points   │   │ Mode Logic   │                   │ │
│  │  │  Landmarks   │   │ DRAW/SELECT  │                   │ │
│  │  └──────────────┘   └──────────────┘                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                   Drawing Layer                         │ │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────────────┐   │ │
│  │  │  Canvas  │ + │    UI    │ → │  Blended Output  │   │ │
│  │  │  Layer   │   │  Header  │   │                  │   │ │
│  │  └──────────┘   └──────────┘   └──────────────────┘   │ │
│  └────────────────────────────────────────────────────────┘ │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                   Output Layer                          │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │              cv2.imshow() Display                │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## Module Dependencies

```
main.py
    ├── hand_detector.py (HandDetector)
    │       └── mediapipe
    │       └── cv2
    ├── canvas.py (Canvas)
    │       └── numpy
    │       └── cv2
    └── ui.py (UI)
            └── cv2
            └── numpy
```

## Data Flow

1. **Input**: Webcam frame captured at 30 FPS
2. **Detection**: MediaPipe processes RGB frame, returns 21 landmarks
3. **Logic**: Finger counter determines DRAW or SELECT mode
4. **Drawing**: Canvas stores persistent drawing, blended with frame
5. **Output**: Final composited frame displayed

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Separate Canvas Layer | Persistent drawing, easy clear/save |
| Bitwise Blending | Faster than addWeighted for real-time |
| Lite Model (complexity=0) | Better FPS on CPU |
| Single Hand Detection | Simpler logic, less processing |
