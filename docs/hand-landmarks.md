# Hand Landmarks - 21 Joints Reference

## MediaPipe Hand Landmark Model

MediaPipe Hands detects **21 3D landmarks** on each hand, representing the skeletal structure.

```
                    THUMB_TIP (4)
                        │
                    THUMB_IP (3)
                        │
                   THUMB_MCP (2)
                        │
                   THUMB_CMC (1)
                        \
                         \
    INDEX_TIP (8)   MIDDLE_TIP (12)   RING_TIP (16)   PINKY_TIP (20)
         │               │                 │               │
    INDEX_DIP (7)   MIDDLE_DIP (11)   RING_DIP (15)   PINKY_DIP (19)
         │               │                 │               │
    INDEX_PIP (6)   MIDDLE_PIP (10)   RING_PIP (14)   PINKY_PIP (18)
         │               │                 │               │
    INDEX_MCP (5)   MIDDLE_MCP (9)    RING_MCP (13)   PINKY_MCP (17)
         \               │                /               /
          \              │               /               /
           \             │              /               /
            -------------│-------------/---------------/
                         │
                     WRIST (0)
```

## Landmark Index Reference

| ID | Name | Joint Type | Description |
|----|------|-----------|-------------|
| 0 | WRIST | Wrist | Base of the hand |
| 1 | THUMB_CMC | Carpometacarpal | Thumb base joint |
| 2 | THUMB_MCP | Metacarpophalangeal | Thumb knuckle |
| 3 | THUMB_IP | Interphalangeal | Thumb middle joint |
| 4 | THUMB_TIP | Tip | Thumb fingertip |
| 5 | INDEX_MCP | Metacarpophalangeal | Index knuckle |
| 6 | INDEX_PIP | Proximal Interphalangeal | Index 1st joint |
| 7 | INDEX_DIP | Distal Interphalangeal | Index 2nd joint |
| 8 | INDEX_TIP | Tip | Index fingertip |
| 9 | MIDDLE_MCP | Metacarpophalangeal | Middle knuckle |
| 10 | MIDDLE_PIP | Proximal Interphalangeal | Middle 1st joint |
| 11 | MIDDLE_DIP | Distal Interphalangeal | Middle 2nd joint |
| 12 | MIDDLE_TIP | Tip | Middle fingertip |
| 13 | RING_MCP | Metacarpophalangeal | Ring knuckle |
| 14 | RING_PIP | Proximal Interphalangeal | Ring 1st joint |
| 15 | RING_DIP | Distal Interphalangeal | Ring 2nd joint |
| 16 | RING_TIP | Tip | Ring fingertip |
| 17 | PINKY_MCP | Metacarpophalangeal | Pinky knuckle |
| 18 | PINKY_PIP | Proximal Interphalangeal | Pinky 1st joint |
| 19 | PINKY_DIP | Distal Interphalangeal | Pinky 2nd joint |
| 20 | PINKY_TIP | Tip | Pinky fingertip |

## Joint Types Explained

### MCP (Metacarpophalangeal)
- The "knuckle" joints
- Connect palm bones (metacarpals) to finger bones (phalanges)
- Allow flexion/extension and abduction/adduction

### PIP (Proximal Interphalangeal)
- The first joint on each finger (closest to palm)
- Hinge joint - only flexion/extension
- Most commonly injured joint in the hand

### DIP (Distal Interphalangeal)
- The second joint on each finger (near fingertip)
- Hinge joint - only flexion/extension
- Smaller range of motion than PIP

### CMC (Carpometacarpal) - Thumb only
- Saddle joint at thumb base
- Allows thumb opposition (touching other fingers)
- Most mobile joint in the thumb

### IP (Interphalangeal) - Thumb only
- Thumb has only one IP joint (not PIP/DIP)
- Equivalent to other fingers' DIP

## Finger Detection Logic

### Detecting Raised Fingers

```python
# For Index, Middle, Ring, Pinky:
# Compare TIP.y with PIP.y (smaller y = higher position)
finger_up = landmarks[TIP].y < landmarks[PIP].y

# For Thumb:
# Compare TIP.x with IP.x (horizontal movement)
thumb_up = landmarks[4].x < landmarks[3].x  # Right hand
thumb_up = landmarks[4].x > landmarks[3].x  # Left hand
```

### Key Landmarks for Gestures

| Gesture | Primary Landmarks |
|---------|------------------|
| Pointing | 8 (INDEX_TIP) |
| Peace Sign | 8, 12 (INDEX_TIP, MIDDLE_TIP) |
| Thumbs Up | 4 (THUMB_TIP) |
| Fist | All TIPs below MCPs |
| Open Palm | All TIPs above MCPs |

## Coordinate System

- **X**: Horizontal position (0.0 = left, 1.0 = right)
- **Y**: Vertical position (0.0 = top, 1.0 = bottom)
- **Z**: Depth (relative to wrist, negative = closer to camera)

All coordinates are normalized to [0.0, 1.0] relative to image dimensions.

## Color Coding (in this project)

| Finger | Color | BGR Value |
|--------|-------|-----------|
| Wrist | White | (255, 255, 255) |
| Thumb | Yellow | (0, 255, 255) |
| Index | Green | (0, 255, 0) |
| Middle | Blue | (255, 0, 0) |
| Ring | Orange | (0, 165, 255) |
| Pinky | Magenta | (255, 0, 255) |

## References

- [MediaPipe Hands Documentation](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)
- [Hand Anatomy Reference](https://en.wikipedia.org/wiki/Hand)
