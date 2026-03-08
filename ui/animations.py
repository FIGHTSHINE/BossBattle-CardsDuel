"""Visual effects and animations."""

from kivy.animation import Animation


class Animations:
    """Collection of animation effects."""
    
    @staticmethod
    def damage_flash(widget):
        """
        Create a flash animation for damage.
        
        Args:
            widget: The widget to animate
        """
        try:
            anim = Animation(
                opacity=0.5, 
                duration=0.1
            ) + Animation(
                opacity=1, 
                duration=0.1
            )
            anim.start(widget)
        except Exception:
            # Ignore animation errors
            pass
    
    @staticmethod
    def color_pulse(widget, color_from, color_to, duration=0.3):
        """
        Create a color pulse animation.
        
        Args:
            widget: The widget to animate
            color_from: Starting color tuple
            color_to: Ending color tuple
            duration: Animation duration in seconds
        """
        try:
            anim = Animation(color=color_to, duration=duration) + \
                   Animation(color=color_from, duration=duration)
            anim.start(widget)
        except Exception:
            pass