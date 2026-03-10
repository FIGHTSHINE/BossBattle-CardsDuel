"""Dynamic boss health bar widget."""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import NumericProperty, ListProperty
from kivy.animation import Animation
from utils.screen_config import ScreenConfig

class BossHealthBar(BoxLayout):
    """Dynamic health bar with color changes and animations."""
    
    hp_percent = NumericProperty(100)
    current_hp = NumericProperty(300)
    max_hp = NumericProperty(300)
    
    def __init__(self, **kwargs):
        """Initialize boss health bar."""
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = ScreenConfig.scale_height(60)
        self.spacing = ScreenConfig.scale_spacing(5)
        
        # HP label
        self.hp_label = Label(
            text=f"BOSS: {self.current_hp}/{self.max_hp}",
            font_size=ScreenConfig.scale_font_size(20),
            size_hint_y=0.3,
            bold=True,
            color=(1, 1, 1, 1),
            halign='left',
            valign='middle'
        )
        self.add_widget(self.hp_label)
        
        # Health bar container (for layout)
        self.health_bar_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.7,
            padding=ScreenConfig.scale_padding(2)
        )
        self.add_widget(self.health_bar_container)
        
        # Background bar (dark gray)
        self.background_bar = Widget(
            size_hint=(1, 1),
            pos=(0, 0)
        )
        with self.background_bar.canvas:
            Color(0.2, 0.2, 0.2, 1)
            self.bg_rect = Rectangle(pos=self.background_bar.pos, 
                                     size=self.background_bar.size)
        self.health_bar_container.add_widget(self.background_bar)
        
        # Foreground bar (health) - Widget that can be animated
        self.foreground_bar = Widget(
            size_hint=(None, 1),
            width=self.health_bar_container.width,
            pos=(0, 0)
        )
        with self.foreground_bar.canvas:
            self.fg_color = Color(0.2, 0.8, 0.3, 1)  # Start with green
            self.fg_rect = Rectangle(pos=self.foreground_bar.pos,
                                     size=self.foreground_bar.size)
        self.health_bar_container.add_widget(self.foreground_bar)
        
        # Border (on top)
        self.border_widget = Widget(
            size_hint=(1, 1),
            pos=(0, 0)
        )
        with self.border_widget.canvas:
            Color(1, 1, 1, 0.5)
            self.border = Line(rectangle=[0, 0, 0, 0], width=2)
        self.health_bar_container.add_widget(self.border_widget)
        
        # Store current color for animations
        self.current_color = (0.2, 0.8, 0.3, 1)
        
        # Bind to position/size changes
        self.background_bar.bind(
            pos=self._update_bg_rect,
            size=self._update_bg_rect
        )
        self.foreground_bar.bind(
            pos=self._update_fg_rect,
            size=self._update_fg_rect
        )
        self.border_widget.bind(
            pos=self._update_border,
            size=self._update_border
        )
        self.health_bar_container.bind(
            size=self._on_container_resize
        )
        
        # Bind to HP changes
        self.bind(hp_percent=self.on_hp_change, 
                  current_hp=self.on_hp_change,
                  max_hp=self.on_hp_change)
        
        # Initial draw
        self._update_all_graphics()
    
    def _on_container_resize(self, instance, value):
        """Handle container resize."""
        # Update background bar size
        self.background_bar.size = value
        self.border_widget.size = value
        self._update_all_graphics()
    
    def _update_bg_rect(self, instance, value):
        """Update background rectangle."""
        self.bg_rect.pos = self.background_bar.pos
        self.bg_rect.size = self.background_bar.size
    
    def _update_fg_rect(self, instance, value):
        """Update foreground rectangle."""
        self.fg_rect.pos = self.foreground_bar.pos
        self.fg_rect.size = self.foreground_bar.size
    
    def _update_border(self, instance, value):
        """Update border rectangle."""
        self.border.rectangle = [
            self.border_widget.x,
            self.border_widget.y,
            self.border_widget.width,
            self.border_widget.height
        ]
    
    def _update_all_graphics(self, *args):
        """Update all graphics."""
        self._update_bg_rect(None, None)
        self._update_fg_rect(None, None)
        self._update_border(None, None)
    
    def on_hp_change(self, instance, value):
        """Handle HP change."""
        # Update text
        self.hp_label.text = f"BOSS: {self.current_hp}/{self.max_hp}"
        
        # Calculate target width
        container_width = self.health_bar_container.width
        target_width = container_width * (self.hp_percent / 100)
        
        # Animate foreground bar width change
        anim = Animation(width=target_width, duration=0.3, t='out_quad')
        anim.start(self.foreground_bar)
        
        # Update color based on HP
        self._update_color()
    
    def _update_color(self):
        """Update health bar color based on HP percentage."""
        if self.hp_percent > 70:
            # Green
            new_color = (0.2, 0.8, 0.3, 1)
        elif self.hp_percent > 30:
            # Yellow
            new_color = (0.9, 0.7, 0.2, 1)
        else:
            # Red
            new_color = (0.9, 0.2, 0.2, 1)
        
        # Directly set the color (no animation)
        self.fg_color.rgba = new_color
    
    
    
    def update_hp(self, current_hp, max_hp):
        """
        Update HP values.
        
        Args:
            current_hp: Current HP value
            max_hp: Maximum HP value
        """
        self.current_hp = current_hp
        self.max_hp = max_hp
        self.hp_percent = (current_hp / max_hp) * 100 if max_hp > 0 else 0