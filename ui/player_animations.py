"""Player widget animations."""

from kivy.animation import Animation
from kivy.clock import Clock


class PlayerAnimations:
    """Handles player widget animations."""
    
    def __init__(self, player_widget, renderer):
        """
        Initialize animations.
        
        Args:
            player_widget: Parent PlayerWidget instance
            renderer: PlayerRenderer instance
        """
        self.widget = player_widget
        self.renderer = renderer
        self.is_attacking = False
        self.base_x = player_widget.x
        self.base_y = player_widget.y
        self.idle_anim_active = False
        self.current_idle_animation = None
    
    def idle_animation(self):
        """Play idle animation (gentle floating up and down)."""
        if self.idle_anim_active:
            return
        
        self.idle_anim_active = True
        
        # Store base position
        self.base_x = self.widget.x
        self.base_y = self.widget.y
        
        # Create floating animation (sine wave motion)
        float_up = Animation(y=self.base_y + 5, duration=0.8, t='in_out_sine')
        float_down = Animation(y=self.base_y, duration=0.8, t='in_out_sine')
        
        # Combine animations
        idle_anim = float_up + float_down
        
        # Use Clock.schedule_once instead of on_complete to avoid recursion
        def restart_idle_animation(dt):
            """Restart idle animation using Clock to avoid recursion."""
            if self.idle_anim_active:
                self.current_idle_animation = idle_anim
                idle_anim.start(self.widget)
                # Schedule next restart after animation completes (1.6 seconds total)
                Clock.schedule_once(restart_idle_animation, 1.6)
        
        # Start the loop
        self.current_idle_animation = idle_anim
        idle_anim.start(self.widget)
        Clock.schedule_once(restart_idle_animation, 1.6)  # 0.8 + 0.8 = 1.6 seconds
    
    def stop_idle_animation(self):
        """Stop the idle animation."""
        if self.current_idle_animation:
            self.current_idle_animation.cancel(self.widget)
            self.current_idle_animation = None
        self.idle_anim_active = False
        
        # Return to base position
        self.widget.y = self.base_y
        self.widget.x = self.base_x
    
    def attack_animation(self):
        """Play attack animation (lunge forward + sword glow)."""
        if self.is_attacking:
            return
        
        self.is_attacking = True
        
        # Stop idle animation temporarily
        self.stop_idle_animation()
        
        # Store base position
        self.base_x = self.widget.x
        self.base_y = self.widget.y
        
        # Forward lunge animation
        lunge_forward = Animation(x=self.base_x + 30, duration=0.15, t='out_quad')
        lunge_backward = Animation(x=self.base_x, duration=0.2, t='in_quad')
        
        # Sword glow animation
        def make_sword_glow(*args):
            """Make sword pixels glow yellow."""
            sword_color = (1, 1, 0.5, 1)  # Bright yellow
            for color in self.renderer.canvas_instructions['sword_pixel_colors']:
                color.rgba = sword_color
        
        def restore_sword_color(*args):
            """Restore sword color to silver."""
            sword_color = (0.9, 0.9, 0.9, 1)  # Silver
            for color in self.renderer.canvas_instructions['sword_pixel_colors']:
                color.rgba = sword_color
            self.is_attacking = False
            # Restart idle animation
            self.idle_animation()
        
        # Schedule sword glow effects
        Clock.schedule_once(make_sword_glow, 0.1)
        Clock.schedule_once(restore_sword_color, 0.35)
        
        # Start lunge animation
        (lunge_forward + lunge_backward).start(self.widget)
    
    def hit_animation(self):
        """Play hit animation when player takes damage (shake + red flash)."""
        # Stop idle animation temporarily
        was_idle = self.idle_anim_active
        self.stop_idle_animation()
        
        # Store base position
        self.base_x = self.widget.x
        self.base_y = self.widget.y
        
        # Shake animation (wiggle back and forth)
        shake1 = Animation(x=self.base_x - 8, duration=0.05)
        shake2 = Animation(x=self.base_x + 8, duration=0.05)
        shake3 = Animation(x=self.base_x - 4, duration=0.05)
        shake4 = Animation(x=self.base_x + 4, duration=0.05)
        return_to_base = Animation(x=self.base_x, duration=0.05)
        
        shake_anim = shake1 + shake2 + shake3 + shake4 + return_to_base
        
        # Red flash animation
        def flash_red(*args):
            """Flash body pixels red."""
            red_color = (1, 0.2, 0.2, 1)
            for color in self.renderer.canvas_instructions['body_pixel_colors']:
                original = tuple(color.rgba)
                color.rgba = red_color
        
        def restore_body_color(*args):
            """Restore body color based on current HP."""
            # Get current state from widget
            state = 'normal'
            if hasattr(self.widget, 'hp_percent'):
                if self.widget.hp_percent <= 30:
                    state = 'critical'
                elif self.widget.hp_percent <= 70:
                    state = 'damaged'
            
            # Restore correct color
            body_color = self.renderer._get_body_color(state)
            for color in self.renderer.canvas_instructions['body_pixel_colors']:
                color.rgba = body_color
            
            # Restart idle animation if it was active
            if was_idle:
                self.idle_animation()
        
        # Schedule flash effects
        Clock.schedule_once(flash_red, 0)
        Clock.schedule_once(restore_body_color, 0.2)
        
        # Start shake animation
        shake_anim.start(self.widget)
    
    def heal_animation(self):
        """Play heal animation (green flash + upward float)."""
        # Stop idle animation temporarily
        was_idle = self.idle_anim_active
        self.stop_idle_animation()
        
        # Store base position
        self.base_x = self.widget.x
        self.base_y = self.widget.y
        
        # Upward float animation
        float_up = Animation(y=self.base_y - 10, duration=0.2, t='out_quad')
        float_down = Animation(y=self.base_y, duration=0.2, t='in_quad')
        
        # Green flash animation
        def flash_green(*args):
            """Flash body pixels bright green."""
            green_color = (0.4, 1, 0.4, 1)
            for color in self.renderer.canvas_instructions['body_pixel_colors']:
                color.rgba = green_color
        
        def restore_body_color(*args):
            """Restore body color based on current HP."""
            state = 'normal'
            if hasattr(self.widget, 'hp_percent'):
                if self.widget.hp_percent <= 30:
                    state = 'critical'
                elif self.widget.hp_percent <= 70:
                    state = 'damaged'
            
            body_color = self.renderer._get_body_color(state)
            for color in self.renderer.canvas_instructions['body_pixel_colors']:
                color.rgba = body_color
            
            # Restart idle animation if it was active
            if was_idle:
                self.idle_animation()
        
        # Schedule flash effects
        Clock.schedule_once(flash_green, 0)
        Clock.schedule_once(restore_body_color, 0.3)
        
        # Start float animation
        (float_up + float_down).start(self.widget)
    
    def shield_break_animation(self):
        """Play shield break animation (flash and disappear)."""
        # Flash shield white
        def flash_white(*args):
            """Flash shield pixels white."""
            white_color = (1, 1, 1, 1)
            for color in self.renderer.canvas_instructions['shield_pixel_colors']:
                color.rgba = white_color
        
        def hide_shield(*args):
            """Hide shield by setting alpha to 0."""
            for color in self.renderer.canvas_instructions['shield_pixel_colors']:
                current = tuple(color.rgba)
                color.rgba = (current[0], current[1], current[2], 0)
        
        Clock.schedule_once(flash_white, 0)
        Clock.schedule_once(hide_shield, 0.15)