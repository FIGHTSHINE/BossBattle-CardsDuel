"""Projectile effects for boss special attacks."""
from functools import partial
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.animation import Animation
from kivy.properties import NumericProperty, ReferenceListProperty, AliasProperty
from kivy.clock import Clock
from kivy.graphics import Line


class FireballProjectile(Widget):
    """
    Fireball projectile that flies from boss to player.
    
    Features:
    - Orange/red circular fireball (25px diameter)
    - Flies from start_pos to target_pos over 0.6 seconds
    - Creates explosion effect on impact
    - Calls on_hit_complete callback when animation finishes
    """
    
    
    """Diameter of the fireball."""
    
    def __init__(self, start_pos, target_pos, on_hit_complete=None, **kwargs):
        """
        Initialize fireball projectile.
        
        Args:
            start_pos: Tuple (x, y) - starting position (boss center)
            target_pos: Tuple (x, y) - target position (player center)
            on_hit_complete: Callback function called when fireball hits target
            **kwargs: Additional widget arguments
        """
        super().__init__(**kwargs)
        
        # Store positions BEFORE setting size (to avoid position reset)
        self._start_pos = start_pos
        self._target_pos = target_pos
        self.on_hit_complete = on_hit_complete
        
        # Set fireball size
        self.size_hint = (None, None)
        self.width = 100
        self.height = 100
        
        # ✅ FIX: Set position AFTER setting size, using start_pos
        # Center the fireball on start_pos
        self.pos = (start_pos[0] - self.width/2, start_pos[1] - self.height/2)
        
        # Colors for fireball
        self.core_color = (1.0, 1.0, 0.0, 1.0)      # Pure yellow core
        self.outer_color = (1.0, 0.5, 0.0, 1.0)     # Bright orange outer
        
        # Debug: Print fireball position
        print(f"[FIREBALL] Created: pos={self.pos}, center=({self.center_x}, {self.center_y})")
        print(f"[FIREBALL] Target: {target_pos}")
        print(f"[FIREBALL] Distance: ({target_pos[0]-start_pos[0]:.1f}, {target_pos[1]-start_pos[1]:.1f})")
        
        # Initialize canvas
        self._init_canvas()
        
        # Schedule flight animation (next frame to ensure widget is added to canvas)
        Clock.schedule_once(lambda _: self._animate_flight(), 0)
    
    def _init_canvas(self):
        """Initialize fireball graphics with glowing effect."""
        with self.canvas:
            # Outer glow (largest, semi-transparent orange-red)
            Color(1.0, 0.4, 0.0, 0.6)  # Orange-red, 60% opacity
            self.outer_glow = Ellipse(
                pos=(self.center_x - self.width * 1.5, self.center_y - self.height * 1.5),
                size=(self.width * 3.0, self.height * 3.0)
            )
            
            # Middle glow (orange-yellow)
            Color(1.0, 0.6, 0.2, 0.8)  # Orange-yellow, 80% opacity
            self.middle_glow = Ellipse(
                pos=(self.center_x - self.width, self.center_y - self.height),
                size=(self.width * 2.0, self.height * 2.0)
            )
            
            # Inner glow (bright yellow)
            Color(1.0, 0.8, 0.3, 0.9)  # Yellow, 90% opacity
            self.inner_glow = Ellipse(
                pos=(self.center_x - self.width * 0.75, self.center_y - self.height * 0.75),
                size=(self.width * 1.5, self.height * 1.5)
            )
            
            # Core (bright yellow-white)
            Color(1.0, 1.0, 0.5, 1.0)  # Bright yellow-white
            self.core = Ellipse(
                pos=(self.center_x - self.width * 0.5, self.center_y - self.height * 0.5),
                size=(self.width, self.height)
            )
            
            # Hot center (white)
            Color(1.0, 1.0, 1.0, 1.0)  # Pure white
            self.hot_center = Ellipse(
                pos=(self.center_x - self.width * 0.35, self.center_y - self.height * 0.35),
                size=(self.width * 0.7, self.height * 0.7)
            )
        
        print(f"[FIREBALL] Canvas initialized: fireball with 5 layers at {self.pos}")
    
    def _animate_flight(self):
        """Animate fireball flying from start to target position."""
        # ✅ FIX: Use stored target_pos and calculate centered position
        """Animate fireball flying from start to target position."""
        # ✅ FIX: Force reset position to stored start position
        start_x = self._start_pos[0] - self.width/2
        start_y = self._start_pos[1] - self.height/2
        self.pos = (start_x, start_y)
    
        # Print debug info
        print(f"[FIREBALL] ========== FLIGHT START ==========")
        print(f"[FIREBALL] Stored start_pos: {self._start_pos}")
        print(f"[FIREBALL] Current pos (before reset): ({self.x:.1f}, {self.y:.1f})")
        print(f"[FIREBALL] Force reset to: ({start_x:.1f}, {start_y:.1f})")
        print(f"[FIREBALL] Center after reset: ({self.center_x:.1f}, {self.center_y:.1f})")
    
        # Calculate target position
        target_x = self._target_pos[0] - self.width/2
        target_y = self._target_pos[1] - self.height/2
        target_pos = (target_x, target_y)
    
        flight_duration = 1.5
    
        print(f"[FIREBALL] Target: {self._target_pos}")
        print(f"[FIREBALL] Flight: FROM ({start_x:.1f}, {start_y:.1f}) TO ({target_x:.1f}, {target_y:.1f})")
        print(f"[FIREBALL] TO pos={target_pos} (center={target_x+self.width/2:.1f}, {target_y+self.height/2:.1f})")
        print(f"[FIREBALL]  duration={flight_duration}s")
        
        # Create flight animation
        flight_anim = Animation(
            pos=target_pos,
            duration=flight_duration,
            t='linear'  # Linear interpolation for consistent speed
        )
        
        # ✅ FIX: Combined progress callback (updates positions and prints)
        def update_progress(animation, widget, progress):
            # Update all canvas elements to follow widget
            cx, cy = self.center_x, self.center_y
            w, h = self.width, self.height
            
            if hasattr(self, 'outer_glow'):
                self.outer_glow.pos = (cx - w * 1.5, cy - h * 1.5)
            if hasattr(self, 'middle_glow'):
                self.middle_glow.pos = (cx - w, cy - h)
            if hasattr(self, 'inner_glow'):
                self.inner_glow.pos = (cx - w * 0.75, cy - h * 0.75)
            if hasattr(self, 'core'):
                self.core.pos = (cx - w * 0.5, cy - h * 0.5)
            if hasattr(self, 'hot_center'):
                self.hot_center.pos = (cx - w * 0.35, cy - h * 0.35)
            
            # Print progress every 25%
            if int(progress * 100) % 25 == 0 and progress > 0:
                print(f"[FIREBALL] Progress: {progress*100:.0f}%, center=({cx:.0f}, {cy:.0f})")
        
        flight_anim.bind(on_progress=update_progress)
        flight_anim.bind(on_complete=self._on_flight_complete)
        
        # Start animation
        flight_anim.start(self)
    
    def _on_flight_complete(self, *args):
        """
        Called when fireball reaches target.
        
        Triggers explosion effect and cleanup.
        """
        print(f"[FIREBALL] Flight complete! Final pos: {self.pos}")
        print(f"[FIREBALL] Final center: ({self.center_x:.1f}, {self.center_y:.1f})")
        print(f"[FIREBALL] Target was: {self._target_pos}")
        
        # Calculate distance to target
        actual_target_x = self._target_pos[0] - self.width/2
        actual_target_y = self._target_pos[1] - self.height/2
        distance_x = actual_target_x - self.x
        distance_y = actual_target_y - self.y
        print(f"[FIREBALL] Distance to target: ({distance_x:.1f}, {distance_y:.1f})")
        
        # Create explosion effect
        self._create_explosion()
        
        # Schedule cleanup after explosion
        Clock.schedule_once(lambda _: self._cleanup(), 0.8)  # ✅ Longer delay
        
        # Call user callback if provided
        if self.on_hit_complete:
            Clock.schedule_once(partial(self.on_hit_complete), 0.3)
    
    def _create_explosion(self):
        """Create explosion visual effect at current position."""
        print(f"[FIREBALL] Creating explosion at pos={self.pos}, center=({self.center_x:.1f}, {self.center_y:.1f})")
        
        # Don't clear canvas - keep fireball visible until explosion expands
        # self.canvas.clear()  # ✅ REMOVED: Don't hide fireball immediately
        
        # Create explosion graphics (add to existing canvas)
        with self.canvas:
            # Explosion outer ring (largest, orange-red)
            Color(1.0, 0.4, 0.0, 0.8)
            self.explosion_outer = Ellipse(
                pos=(self.center_x - 20, self.center_y - 20),
                size=(40, 40)
            )
            
            # Explosion middle ring (yellow-orange)
            Color(1.0, 0.7, 0.2, 0.9)
            self.explosion_middle = Ellipse(
                pos=(self.center_x - 15, self.center_y - 15),
                size=(30, 30)
            )
            
            # Explosion inner ring (bright yellow-white)
            Color(1.0, 1.0, 0.5, 1.0)
            self.explosion_inner = Ellipse(
                pos=(self.center_x - 10, self.center_y - 10),
                size=(20, 20)
            )
        
        # Animate explosion (gradual expansion)
        expand_outer = Animation(
            size=(120, 120),
            pos=(self.center_x - 60, self.center_y - 60),
            duration=0.4,  # ✅ Longer duration
            t='out_quad'
        )
        
        expand_middle = Animation(
            size=(100, 100),
            pos=(self.center_x - 50, self.center_y - 50),
            duration=0.4,
            t='out_quad'
        )
        
        expand_inner = Animation(
            size=(80, 80),
            pos=(self.center_x - 40, self.center_y - 40),
            duration=0.4,
            t='out_quad'
        )
        
        # Fade out explosion
        fade_anim = Animation(opacity=0, duration=0.3)  # ✅ Longer fade
        
        # Start all expansions
        expand_outer.start(self.explosion_outer)
        expand_middle.start(self.explosion_middle)
        expand_inner.start(self.explosion_inner)
        
        # After expansion, fade out
        expand_inner.bind(on_complete=lambda *args: fade_anim.start(self))
        
        print(f"[FIREBALL] Explosion animation started")
    
    def _cleanup(self):
        """Remove projectile from parent widget."""
        if self.parent:
            self.parent.remove_widget(self)


class ProjectileManager:
    """
    Manager class for spawning and controlling projectiles.
    
    Provides a convenient interface for creating projectiles
    without manually managing widget lifecycle.
    """
    
    @staticmethod
    def create_fireball(start_widget, end_widget, parent_widget, on_hit_complete=None):
        """
        Create a fireball projectile from one widget to another.
        
        Args:
            start_widget: Widget to launch from (e.g., boss_widget)
            end_widget: Widget to target (e.g., player_widget)
            parent_widget: Parent widget to add projectile to (e.g., game_screen)
            on_hit_complete: Callback when fireball hits target
            
        Returns:
            FireballProjectile: The created projectile instance
        """
        # Calculate center positions
        start_pos = (
            start_widget.x + start_widget.width / 2,
            start_widget.y + start_widget.height / 2
        )
        
        end_pos = (
            end_widget.x + end_widget.width / 2,
            end_widget.y + end_widget.height / 2
        )
        
        # Create projectile
        projectile = FireballProjectile(
            start_pos=start_pos,
            target_pos=end_pos,
            on_hit_complete=on_hit_complete
        )
        
        # Add to parent widget (on top of other elements)
        parent_widget.add_widget(projectile)
        
        return projectile