"""Fireball animation control."""

from kivy.animation import Animation
from kivy.clock import Clock
from functools import partial


class FireballAnimation:
    """Handles fireball animations."""
    
    def __init__(self, projectile):
        """Initialize animation handler."""
        self.projectile = projectile
    
    def animate_flight(self):
        """Animate fireball flying from start to target position."""
        p = self.projectile
        
        # Reset position
        start_x = p._start_pos[0] - p.width/2
        start_y = p._start_pos[1] - p.height/2
        p.pos = (start_x, start_y)
        
        # Calculate target position
        target_x = p._target_pos[0] - p.width/2
        target_y = p._target_pos[1] - p.height/2
        target_pos = (target_x, target_y)
        
        flight_duration = 1.5
        
        # Create flight animation
        flight_anim = Animation(
            pos=target_pos,
            duration=flight_duration,
            t='linear'
        )
        
        # Bind callbacks
        flight_anim.bind(on_progress=self._update_progress)
        flight_anim.bind(on_complete=self._on_flight_complete)
        
        # Start animation
        flight_anim.start(p)
    
    def _update_progress(self, animation, widget, progress):
        """Update canvas positions during flight."""
        self.projectile.graphics.update_canvas_positions()
    
    def _on_flight_complete(self, *args):
        """Called when fireball reaches target."""
        p = self.projectile
        
        print(f"[FIREBALL] Flight complete!")
        
        # Create explosion
        p.graphics.create_explosion_effect()
        self.animate_explosion()
        
        # Schedule cleanup
        Clock.schedule_once(lambda _: p._cleanup(), 0.8)
        
        # Call user callback
        if p.on_hit_complete:
            Clock.schedule_once(partial(p.on_hit_complete), 0.3)
    
    def animate_explosion(self):
        """Animate explosion expansion and fade."""
        p = self.projectile
        
        # Expand animations
        expand_outer = Animation(
            size=(120, 120),
            pos=(p.center_x - 60, p.center_y - 60),
            duration=0.4,
            t='out_quad'
        )
        
        expand_middle = Animation(
            size=(100, 100),
            pos=(p.center_x - 50, p.center_y - 50),
            duration=0.4,
            t='out_quad'
        )
        
        expand_inner = Animation(
            size=(80, 80),
            pos=(p.center_x - 40, p.center_y - 40),
            duration=0.4,
            t='out_quad'
        )
        
        # Fade out
        fade_anim = Animation(opacity=0, duration=0.3)
        
        # Start animations
        expand_outer.start(p.explosion_outer)
        expand_middle.start(p.explosion_middle)
        expand_inner.start(p.explosion_inner)
        
        # Fade after expansion
        expand_inner.bind(on_complete=lambda *args: fade_anim.start(p))