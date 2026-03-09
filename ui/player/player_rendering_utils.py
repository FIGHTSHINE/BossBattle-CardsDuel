"""Rendering utilities for player widget."""

from kivy.graphics import Color, Rectangle
from ui.player.player_pixel_patterns import (
    BODY_PATTERN, SWORD_PATTERN, SHIELD_PATTERN, CAPE_PATTERN,
    BODY_COLORS, AURA_COLORS, EYE_COLORS, CAPE_COLORS, SWORD_COLORS, SHIELD_COLOR
)


class PlayerRenderingUtils:
    """Utility class for player rendering operations."""
    
    def __init__(self, renderer):
        """
        Initialize rendering utilities.
        
        Args:
            renderer: Parent PlayerRenderer instance
        """
        self.renderer = renderer
        self.widget = renderer.widget
        self.canvas_instructions = renderer.canvas_instructions
        self.pixel_size = renderer.pixel_size
    
    def init_body_pixels(self):
        """Initialize body pixel blocks (6x5 grid for chest/body)."""
        for row_idx, row in enumerate(BODY_PATTERN):
            for col_idx, pixel in enumerate(row):
                if pixel:
                    with self.widget.canvas:
                        color = Color(*BODY_COLORS['normal'])
                        rect = Rectangle(pos=(0, 0), size=(self.pixel_size, self.pixel_size))
                        self.canvas_instructions['body_pixel_colors'].append(color)
                        self.canvas_instructions['body_pixels'].append(rect)
    
    def init_sword_pixels(self):
        """Initialize sword pixel blocks (3x7 grid)."""
        for row_idx, row in enumerate(SWORD_PATTERN):
            for col_idx, pixel in enumerate(row):
                if pixel:
                    with self.widget.canvas:
                        color = Color(*SWORD_COLORS['normal'])
                        rect = Rectangle(pos=(0, 0), size=(self.pixel_size, self.pixel_size))
                        self.canvas_instructions['sword_pixel_colors'].append(color)
                        self.canvas_instructions['sword_pixels'].append(rect)
    
    def init_shield_pixels(self):
        """Initialize shield pixel blocks (4x4 grid)."""
        for row_idx, row in enumerate(SHIELD_PATTERN):
            for col_idx, pixel in enumerate(row):
                if pixel:
                    with self.widget.canvas:
                        color = Color(*SHIELD_COLOR)
                        rect = Rectangle(pos=(0, 0), size=(self.pixel_size, self.pixel_size))
                        self.canvas_instructions['shield_pixel_colors'].append(color)
                        self.canvas_instructions['shield_pixels'].append(rect)
    
    def init_cape_pixels(self):
        """Initialize cape pixel blocks (3x5 grid)."""
        for row_idx, row in enumerate(CAPE_PATTERN):
            for col_idx, pixel in enumerate(row):
                if pixel:
                    with self.widget.canvas:
                        color = Color(*CAPE_COLORS['normal'])
                        rect = Rectangle(pos=(0, 0), size=(self.pixel_size, self.pixel_size))
                        self.canvas_instructions['cape_pixel_colors'].append(color)
                        self.canvas_instructions['cape_pixels'].append(rect)
    
    def update_aura(self, state):
        """Update aura based on state."""
        aura_size = (self.widget.width * 1.2, self.widget.height * 1.2)
        aura_pos = (self.widget.x - (aura_size[0] - self.widget.width) / 2,
                    self.widget.y - (aura_size[1] - self.widget.height) / 2)
        
        self.canvas_instructions['aura'].pos = aura_pos
        self.canvas_instructions['aura'].size = aura_size
        self.canvas_instructions['aura_color'].rgba = AURA_COLORS[state]
    
    def get_body_color(self, state):
        """Get body color based on state."""
        return BODY_COLORS[state]
    
    def update_body_pixels(self, state, center_x, center_y):
        """Update body pixel positions and colors."""
        body_color = self.get_body_color(state)
        pixel_idx = 0
        start_x = center_x - (6 * self.pixel_size) / 2
        start_y = center_y - (7 * self.pixel_size) / 2
        
        for row_idx, row in enumerate(BODY_PATTERN):
            for col_idx, pixel in enumerate(row):
                if pixel:
                    if pixel_idx < len(self.canvas_instructions['body_pixels']):
                        x = start_x + col_idx * self.pixel_size
                        y = start_y + row_idx * self.pixel_size
                        self.canvas_instructions['body_pixels'][pixel_idx].pos = (x, y)
                        self.canvas_instructions['body_pixel_colors'][pixel_idx].rgba = body_color
                        pixel_idx += 1
    
    def update_eyes(self, center_x, center_y, state):
        """Update eye positions and colors."""
        eye_offset = self.pixel_size * 2
        eye_color = EYE_COLORS[state]
        
        self.canvas_instructions['left_eye_color'].rgba = eye_color
        self.canvas_instructions['right_eye_color'].rgba = eye_color
        
        eye_y = center_y - self.pixel_size
        self.canvas_instructions['left_eye'].pos = (center_x - eye_offset - self.pixel_size, eye_y)
        self.canvas_instructions['right_eye'].pos = (center_x + eye_offset, eye_y)
    
    def update_sword_pixels(self, center_x, center_y, state):
        """Update sword pixel positions and colors."""
        sword_color = SWORD_COLORS.get(state, SWORD_COLORS['normal'])
        pixel_idx = 0
        start_x = center_x + self.pixel_size * 3
        start_y = center_y - self.pixel_size * 3
        
        for row_idx, row in enumerate(SWORD_PATTERN):
            for col_idx, pixel in enumerate(row):
                if pixel:
                    if pixel_idx < len(self.canvas_instructions['sword_pixels']):
                        x = start_x + col_idx * self.pixel_size
                        y = start_y + row_idx * self.pixel_size
                        self.canvas_instructions['sword_pixels'][pixel_idx].pos = (x, y)
                        self.canvas_instructions['sword_pixel_colors'][pixel_idx].rgba = sword_color
                        pixel_idx += 1
    
    def update_shield_pixels(self, center_x, center_y, shield):
        """Update shield pixels (only shown when shield > 0)."""
        shield_visible = shield > 0
        shield_alpha = 1.0 if shield_visible else 0.0
        shield_color = (*SHIELD_COLOR[:3], shield_alpha)
        
        pixel_idx = 0
        start_x = center_x - self.pixel_size * 6
        start_y = center_y - self.pixel_size * 2
        
        for row_idx, row in enumerate(SHIELD_PATTERN):
            for col_idx, pixel in enumerate(row):
                if pixel:
                    if pixel_idx < len(self.canvas_instructions['shield_pixels']):
                        x = start_x + col_idx * self.pixel_size
                        y = start_y + row_idx * self.pixel_size
                        self.canvas_instructions['shield_pixels'][pixel_idx].pos = (x, y)
                        self.canvas_instructions['shield_pixel_colors'][pixel_idx].rgba = shield_color
                        pixel_idx += 1
    
    def update_cape_pixels(self, center_x, center_y, state):
        """Update cape pixel positions."""
        cape_color = CAPE_COLORS[state]
        pixel_idx = 0
        start_x = center_x - self.pixel_size * 1.5
        start_y = center_y + self.pixel_size * 2
        
        for row_idx, row in enumerate(CAPE_PATTERN):
            for col_idx, pixel in enumerate(row):
                if pixel:
                    if pixel_idx < len(self.canvas_instructions['cape_pixels']):
                        x = start_x + col_idx * self.pixel_size
                        y = start_y + row_idx * self.pixel_size
                        self.canvas_instructions['cape_pixels'][pixel_idx].pos = (x, y)
                        self.canvas_instructions['cape_pixel_colors'][pixel_idx].rgba = cape_color
                        pixel_idx += 1