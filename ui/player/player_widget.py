"""Player widget with pixel art graphics."""

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.clock import Clock
from ui.player.player_renderer import PlayerRenderer
from ui.player.player_animations import PlayerAnimations
from utils.screen_config import ScreenConfig

class PlayerWidget(Widget):
    """Pixel art player graphics widget with state-based visuals."""
    
    hp_percent = NumericProperty(100)
    shield = NumericProperty(0)
    
    def __init__(self, **kwargs):
        """Initialize player widget."""
        super().__init__(**kwargs)
        
        # Set fixed size (slightly smaller than boss)
        self.size_hint = (None, None)
        self.size = ScreenConfig.calculate_player_size()
        
        # State tracking
        self.state = 'normal'  # normal, damaged, critical, attacking
        
        # Initialize components
        self.renderer = PlayerRenderer(self)
        self.animations = PlayerAnimations(self, self.renderer)
        
        # Initialize canvas
        self.renderer.init_canvas()
        
        # Bind to property changes
        self.bind(pos=self._on_property_change, 
                  size=self._on_property_change, 
                  hp_percent=self._on_hp_change,
                  shield=self._on_shield_change)
        
        # Initial draw
        self._update_display()
        
        # Start idle animation after a short delay
        Clock.schedule_once(lambda dt: self.animations.idle_animation(), 0.5)
    
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
    
    def _on_shield_change(self, instance, value):
        """Handle shield change."""
        # Update display to show/hide shield
        self._update_display()
    
    def _on_property_change(self, *args):
        """Handle position or size change."""
        # Update base position for animations
        if hasattr(self.animations, 'base_x'):
            self.animations.base_x = self.x
            self.animations.base_y = self.y
        
        self._update_display()
    
    def _update_display(self):
        """Update player display."""
        self.renderer.update_graphics(self.state, self.hp_percent, self.shield)
    
    def attack_animation(self):
        """Play attack animation."""
        self.animations.attack_animation()
    
    def hit_animation(self):
        """Play hit animation when taking damage."""
        self.animations.hit_animation()
    
    def heal_animation(self):
        """Play heal animation when healing."""
        self.animations.heal_animation()
    
    def shield_break_animation(self):
        """Play shield break animation."""
        self.animations.shield_break_animation()