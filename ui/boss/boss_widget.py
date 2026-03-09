"""Boss widget with procedural graphics."""

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

# from boss_battle.ui.boss.boss_renderer import BossRenderer
# from boss_battle.ui.boss.boss_animations import BossAnimations
from ui.boss.boss_renderer import BossRenderer
from ui.boss.boss_animations import BossAnimations

class BossWidget(Widget):
    """Procedural boss graphics widget with state-based visuals."""
    
    hp_percent = NumericProperty(100)
    
    def __init__(self, **kwargs):
        """Initialize boss widget."""
        super().__init__(**kwargs)
        
        # Set fixed size
        self.size_hint = (None, None)
        self.size = (100, 100)
        
        # State tracking
        self.state = 'normal'  # normal, damaged, critical
        
        # Initialize components
        self.renderer = BossRenderer(self)
        self.animations = BossAnimations(self, self.renderer)
        
        # Initialize canvas
        self.renderer.init_canvas()
        
        # Bind to property changes
        self.bind(pos=self._on_property_change, 
                  size=self._on_property_change, 
                  hp_percent=self._on_hp_change)
        
        # Initial draw
        self._update_display()
    
    def _on_hp_change(self, instance, value):
        """Handle HP percent change."""
        old_state = self.state
        
        if value > 70:
            self.state = 'normal'
        elif value > 30:
            self.state = 'damaged'
        else:
            self.state = 'critical'
        
        if old_state != self.state:
            self._update_display()
    
    def _on_property_change(self, *args):
        """Handle position or size change."""
        self._update_display()
    
    def _update_display(self):
        """Update boss display."""
        self.renderer.update_graphics(self.state, self.hp_percent)
    
    def attack_animation(self):
        """Play attack animation."""
        self.animations.attack_animation()
    
    def hit_animation(self):
        """Play hit animation."""
        self.animations.hit_animation()