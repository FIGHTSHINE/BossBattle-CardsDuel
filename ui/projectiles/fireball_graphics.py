"""Fireball graphics rendering."""

from kivy.graphics import Color, Ellipse


class FireballGraphics:
    """Handles fireball visual rendering."""
    
    def __init__(self, projectile):
        """Initialize graphics handler."""
        self.projectile = projectile
    
    def init_fireball_canvas(self):
        """Initialize fireball graphics with glowing effect."""
        p = self.projectile
        
        with p.canvas:
            # Outer glow
            Color(1.0, 0.4, 0.0, 0.6)
            p.outer_glow = Ellipse(
                pos=(p.center_x - p.width * 1.5, p.center_y - p.height * 1.5),
                size=(p.width * 3.0, p.height * 3.0)
            )
            
            # Middle glow
            Color(1.0, 0.6, 0.2, 0.8)
            p.middle_glow = Ellipse(
                pos=(p.center_x - p.width, p.center_y - p.height),
                size=(p.width * 2.0, p.height * 2.0)
            )
            
            # Inner glow
            Color(1.0, 0.8, 0.3, 0.9)
            p.inner_glow = Ellipse(
                pos=(p.center_x - p.width * 0.75, p.center_y - p.height * 0.75),
                size=(p.width * 1.5, p.height * 1.5)
            )
            
            # Core
            Color(1.0, 1.0, 0.5, 1.0)
            p.core = Ellipse(
                pos=(p.center_x - p.width * 0.5, p.center_y - p.height * 0.5),
                size=(p.width, p.height)
            )
            
            # Hot center
            Color(1.0, 1.0, 1.0, 1.0)
            p.hot_center = Ellipse(
                pos=(p.center_x - p.width * 0.35, p.center_y - p.height * 0.35),
                size=(p.width * 0.7, p.height * 0.7)
            )
    
    def create_explosion_effect(self):
        """Create explosion visual effect at current position."""
        p = self.projectile
        
        with p.canvas:
            # Explosion outer ring
            Color(1.0, 0.4, 0.0, 0.8)
            p.explosion_outer = Ellipse(
                pos=(p.center_x - 20, p.center_y - 20),
                size=(40, 40)
            )
            
            # Explosion middle ring
            Color(1.0, 0.7, 0.2, 0.9)
            p.explosion_middle = Ellipse(
                pos=(p.center_x - 15, p.center_y - 15),
                size=(30, 30)
            )
            
            # Explosion inner ring
            Color(1.0, 1.0, 0.5, 1.0)
            p.explosion_inner = Ellipse(
                pos=(p.center_x - 10, p.center_y - 10),
                size=(20, 20)
            )
    
    def update_canvas_positions(self):
        """Update all canvas elements to follow widget position."""
        p = self.projectile
        cx, cy = p.center_x, p.center_y
        w, h = p.width, p.height
        
        if hasattr(p, 'outer_glow'):
            p.outer_glow.pos = (cx - w * 1.5, cy - h * 1.5)
        if hasattr(p, 'middle_glow'):
            p.middle_glow.pos = (cx - w, cy - h)
        if hasattr(p, 'inner_glow'):
            p.inner_glow.pos = (cx - w * 0.75, cy - h * 0.75)
        if hasattr(p, 'core'):
            p.core.pos = (cx - w * 0.5, cy - h * 0.5)
        if hasattr(p, 'hot_center'):
            p.hot_center.pos = (cx - w * 0.35, cy - h * 0.35)