"""
UI Module - Menu and visual elements
"""
import cv2
import numpy as np


class UI:
    """Handle UI elements like menu, buttons, cursor."""

    # Color definitions (BGR format for OpenCV)
    COLORS = {
        'red': (0, 0, 255),
        'blue': (255, 0, 0),
        'purple': (255, 0, 128),
        'green': (0, 255, 0),
        'yellow': (0, 255, 255),
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'gray': (50, 50, 50),
        'eraser': (0, 0, 0)
    }

    BRUSH_SIZES = {
        'small': 5,
        'medium': 15,
        'large': 25,
        'eraser': 50
    }

    def __init__(self, width, height, header_height=100):
        self.width = width
        self.height = height
        self.header_height = header_height

        # Menu items: (name, color_key, x_start, x_end)
        self.menu_items = self._create_menu_items()

        # Current selection
        self.current_color = self.COLORS['red']
        self.current_thickness = self.BRUSH_SIZES['medium']
        self.is_eraser = False
        self.selected_index = 0

    def _create_menu_items(self):
        """Create menu item positions."""
        items = []
        names = ['RED', 'BLUE', 'PURPLE', 'GREEN', 'ERASER', 'CLEAR']
        colors = ['red', 'blue', 'purple', 'green', 'eraser', 'black']

        item_width = self.width // len(names)
        for i, (name, color) in enumerate(zip(names, colors)):
            items.append({
                'name': name,
                'color_key': color,
                'x_start': i * item_width,
                'x_end': (i + 1) * item_width,
                'color': self.COLORS[color]
            })
        return items

    def draw_header(self, frame):
        """Draw the menu header on frame."""
        # Dark background
        cv2.rectangle(frame, (0, 0), (self.width, self.header_height),
                     self.COLORS['gray'], -1)

        # Draw menu items
        for i, item in enumerate(self.menu_items):
            x_center = (item['x_start'] + item['x_end']) // 2
            y_center = self.header_height // 2

            # Draw color circle or icon
            if item['name'] == 'CLEAR':
                # Draw X for clear
                cv2.putText(frame, 'X', (x_center - 15, y_center + 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, self.COLORS['white'], 2)
            elif item['name'] == 'ERASER':
                # Draw eraser rectangle
                cv2.rectangle(frame, (x_center - 20, y_center - 15),
                             (x_center + 20, y_center + 15), self.COLORS['white'], -1)
            else:
                # Draw color circle
                cv2.circle(frame, (x_center, y_center), 25, item['color'], -1)

            # Draw label
            label_x = x_center - len(item['name']) * 5
            cv2.putText(frame, item['name'], (label_x, self.header_height - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS['white'], 1)

            # Highlight selected
            if i == self.selected_index:
                cv2.rectangle(frame, (item['x_start'] + 5, 5),
                             (item['x_end'] - 5, self.header_height - 5),
                             self.COLORS['green'], 3)

        # Draw current brush size indicator
        cv2.circle(frame, (self.width - 40, self.header_height // 2),
                  self.current_thickness, self.current_color, -1)

        return frame

    def check_menu_selection(self, x, y):
        """Check if position is in menu and handle selection."""
        if y > self.header_height:
            return False

        for i, item in enumerate(self.menu_items):
            if item['x_start'] <= x < item['x_end']:
                self.selected_index = i

                if item['name'] == 'CLEAR':
                    return 'clear'
                elif item['name'] == 'ERASER':
                    self.is_eraser = True
                    self.current_thickness = self.BRUSH_SIZES['eraser']
                    return 'eraser'
                else:
                    self.is_eraser = False
                    self.current_color = item['color']
                    self.current_thickness = self.BRUSH_SIZES['medium']
                    return 'color'

        return False

    def draw_cursor(self, frame, x, y, mode='draw'):
        """Draw cursor indicator at finger position."""
        if mode == 'select':
            # Selection mode - two fingers
            cv2.circle(frame, (x, y), 15, self.COLORS['yellow'], 2)
        else:
            # Drawing mode - one finger
            color = self.COLORS['white'] if self.is_eraser else self.current_color
            cv2.circle(frame, (x, y), self.current_thickness // 2, color, 2)

        return frame

    def draw_mode_indicator(self, frame, mode):
        """Show current mode on screen."""
        text = "SELECT" if mode == 'select' else "DRAW"
        color = self.COLORS['yellow'] if mode == 'select' else self.COLORS['green']
        cv2.putText(frame, text, (10, self.height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        return frame
