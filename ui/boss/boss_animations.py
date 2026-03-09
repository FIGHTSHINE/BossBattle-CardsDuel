"""Boss widget animations."""

from kivy.animation import Animation
from kivy.clock import Clock
# from boss_battle.ui.boss.boss_special_effects import BossSpecialEffectManager
from ui.boss.boss_special_effects import BossSpecialEffectManager

class BossAnimations:
    """Handles boss widget animations."""
    
    def __init__(self, boss_widget, renderer):
        """
        Initialize animations.
        
        Args:
            boss_widget: Parent BossWidget instance
            renderer: BossRenderer instance
        """
        self.widget = boss_widget
        self.renderer = renderer
        self.is_attacking = False
    
    def attack_animation(self):
        """Play attack animation (shake and flash)."""
        if self.is_attacking:
            return
        
        self.is_attacking = True
        
        # Shake animation
        anim = Animation(x=self.widget.x - 10, duration=0.05)
        anim += Animation(x=self.widget.x + 10, duration=0.05)
        anim += Animation(x=self.widget.x, duration=0.05)
        
        # Flash animation
        original_color = tuple(self.renderer.canvas_instructions['body_color'].rgba)
        
        def flash_on(*args):
            self.renderer.canvas_instructions['body_color'].rgba = (1, 1, 1, 1)
        
        def flash_off(*args):
            self.renderer.canvas_instructions['body_color'].rgba = original_color
            self.is_attacking = False
        
        Clock.schedule_once(flash_on, 0.1)
        Clock.schedule_once(flash_off, 0.15)
        
        anim.start(self.widget)
    
    def hit_animation(self):
        """Play hit animation when boss takes damage."""
        original_color = tuple(self.renderer.canvas_instructions['body_color'].rgba)
        
        self.renderer.canvas_instructions['body_color'].rgba = (1, 1, 1, 1)
        
        def restore(*args):
            self.renderer.canvas_instructions['body_color'].rgba = original_color
        
        Clock.schedule_once(restore, 0.1)
        
    def special_attack_animation(self, player_widget, parent_widget, callback=None):
        """
        Play boss special attack animation with projectile.
        
        This method coordinates the complete special attack sequence:
        1. Boss charging animation (glowing/pulsing)
        2. Fireball projectile launch
        3. Explosion effect on player
        4. Trigger completion callback
        
        Args:
            player_widget: Target player widget
            parent_widget: Parent widget to add projectile effects to
            callback: Optional callback function when attack completes
        """
        if self.is_attacking:
            # Don't interrupt ongoing attack
            return
        
        # Mark that boss is attacking
        self.is_attacking = True
        
        # Create special effects manager
        effects_manager = BossSpecialEffectManager()
        
        # Define wrapper callback to reset attack flag and call user callback
        def complete_callback():
            self.is_attacking = False
            if callback:
                callback()
        
        # Execute complete special attack sequence
        effects_manager.fireball_special_attack(
            boss_widget=self.widget,
            player_widget=player_widget,
            parent_widget=parent_widget,
            callback=complete_callback
        )