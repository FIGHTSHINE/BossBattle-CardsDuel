"""Player widget canvas renderer - Pixel art style."""

from kivy.graphics import Color, Rectangle, Line
from ui.player_rendering_utils import PlayerRenderingUtils


class PlayerRenderer:
    """Handles canvas drawing for player widget using pixel art style."""
    
    def __init__(self, player_widget):
        """
        Initialize renderer.
        
        Args:
            player_widget: Parent PlayerWidget instance
        """
        self.widget = player_widget
        self.canvas_instructions = {}
        self.pixel_size = 6  # Size of each "pixel" block
        
        # Initialize rendering utilities
        self.utils = PlayerRenderingUtils(self)
    
    def init_canvas(self):
        """Initialize all canvas instructions for pixel art player."""
        with self.widget.canvas:
            # Background glow (aura)
            self.canvas_instructions['aura_color'] = Color(0.2, 0.8, 0.3, 0.2)
            self.canvas_instructions['aura'] = Rectangle(pos=self.widget.pos, size=self.widget.size)
            
            # Pixel blocks for body parts
            self.canvas_instructions['body_pixels'] = []
            self.canvas_instructions['body_pixel_colors'] = []
            
            # Eyes
            self.canvas_instructions['left_eye_color'] = Color(1, 1, 1, 1)
            self.canvas_instructions['left_eye'] = Rectangle(pos=(0, 0), size=(self.pixel_size, self.pixel_size))
            
            self.canvas_instructions['right_eye_color'] = Color(1, 1, 1, 1)
            self.canvas_instructions['right_eye'] = Rectangle(pos=(0, 0), size=(self.pixel_size, self.pixel_size))
            
            # Sword
            self.canvas_instructions['sword_pixels'] = []
            self.canvas_instructions['sword_pixel_colors'] = []
            
            # Shield
            self.canvas_instructions['shield_pixels'] = []
            self.canvas_instructions['shield_pixel_colors'] = []
            
            # Cape
            self.canvas_instructions['cape_color'] = Color(0.1, 0.3, 0.6, 1)
            self.canvas_instructions['cape_pixels'] = []
            self.canvas_instructions['cape_pixel_colors'] = []
        
        # Initialize pixel patterns using utilities
        self.utils.init_body_pixels()
        self.utils.init_sword_pixels()
        self.utils.init_shield_pixels()
        self.utils.init_cape_pixels()
    
    def update_graphics(self, state, hp_percent, shield):
        """
        Update all graphics based on state and shield.
        
        Args:
            state: 'normal', 'damaged', or 'critical'
            hp_percent: Current HP percentage
            shield: Current shield value
        """
        center_x = self.widget.x + self.widget.width / 2
        center_y = self.widget.y + self.widget.height / 2
        
        # Update all graphics using utilities
        self.utils.update_aura(state)
        self.utils.update_body_pixels(state, center_x, center_y)
        self.utils.update_eyes(center_x, center_y, state)
        self.utils.update_sword_pixels(center_x, center_y, state)
        self.utils.update_shield_pixels(center_x, center_y, shield)
        self.utils.update_cape_pixels(center_x, center_y, state)
    
    def _get_body_color(self, state):
        """
        Get body color for given state (backward compatibility).
        
        Args:
            state: 'normal', 'damaged', or 'critical'
            
        Returns:
            tuple: RGBA color tuple
        """
        return self.utils.get_body_color(state)