"""Fireball projectile core class."""

from kivy.uix.widget import Widget
from kivy.clock import Clock
# ✅ 使用相对导入
from .fireball_graphics import FireballGraphics
from .fireball_animation import FireballAnimation


class FireballProjectile(Widget):
    """Fireball projectile that flies from boss to player."""
    
    def __init__(self, start_pos, target_pos, on_hit_complete=None, **kwargs):
        super().__init__(**kwargs)
        
        # Core properties
        self._start_pos = start_pos
        self._target_pos = target_pos
        self.on_hit_complete = on_hit_complete
        self.size_hint = (None, None)
        self.width = 100
        self.height = 100
        self.pos = (start_pos[0] - self.width/2, start_pos[1] - self.height/2)
        
        # Colors
        self.core_color = (1.0, 1.0, 0.0, 1.0)
        self.outer_color = (1.0, 0.5, 0.0, 1.0)
        
        # Graphics and animation handlers
        self.graphics = FireballGraphics(self)
        self.animation = FireballAnimation(self)
        
        # Initialize canvas
        self.graphics.init_fireball_canvas()
        
        # Schedule animation
        Clock.schedule_once(lambda _: self.animation.animate_flight(), 0)
    
    def _cleanup(self):
        """Remove projectile from parent widget."""
        if self.parent:
            self.parent.remove_widget(self)