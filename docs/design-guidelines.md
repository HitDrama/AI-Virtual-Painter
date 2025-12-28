# AI Virtual Painter - Design Guidelines

## UI Layout

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER MENU (Height: 100px)                                │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐ │
│  │ RED  │ │ BLUE │ │PURPLE│ │GREEN │ │ERASER│ │  CLEAR   │ │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────────┘ │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    DRAWING CANVAS AREA                      │
│                    (Webcam Feed + Overlay)                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Color Palette (BGR Format - OpenCV)

| Element | Color | BGR | Purpose |
|---------|-------|-----|---------|
| Red Brush | Red | (0, 0, 255) | Drawing |
| Blue Brush | Blue | (255, 0, 0) | Drawing |
| Purple Brush | Purple | (255, 0, 128) | Drawing |
| Green Brush | Green | (0, 255, 0) | Drawing |
| Eraser | Black | (0, 0, 0) | Erase |
| Menu BG | Dark Gray | (50, 50, 50) | UI |
| Selection | Green | (0, 255, 0) | Highlight |

## Brush Sizes

| Mode | Pixels | Use Case |
|------|--------|----------|
| Small | 5 | Fine details |
| Medium | 15 | Normal drawing (default) |
| Large | 25 | Bold strokes |
| Eraser | 50 | Quick erase |

## Gesture Mapping

| Fingers | Mode | Action |
|---------|------|--------|
| Index only | Draw | Draw at fingertip |
| Index + Middle | Select | Choose color/tool |
| Other | Idle | No action |

## Visual Feedback

- Green border around selected menu item
- Circle cursor at fingertip
- Mode indicator at bottom-left (DRAW/SELECT)
