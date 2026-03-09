"""Screen configuration and responsive layout utilities."""

from kivy.core.window import Window
from kivy.logger import Logger
from kivy.metrics import Metrics


class ScreenConfig:
    """Manage screen configuration and responsive layouts."""
    
    # Screen size breakpoints
    TABLET_WIDTH = 600  # pixels
    PHONE_WIDTH = 360   # pixels
    
    @staticmethod
    def get_screen_orientation():
        """
        Get current screen orientation.
        
        Returns:
            str: 'landscape' or 'portrait'
        """
        width, height = Window.size
        return 'landscape' if width > height else 'portrait'
    
    @staticmethod
    def is_landscape():
        """Check if current orientation is landscape."""
        return ScreenConfig.get_screen_orientation() == 'landscape'
    
    @staticmethod
    def is_portrait():
        """Check if current orientation is portrait."""
        return ScreenConfig.get_screen_orientation() == 'portrait'
    
    @staticmethod
    def get_screen_size_category():
        """
        Get screen size category.
        
        Returns:
            str: 'tablet', 'phone', or 'desktop'
        """
        width, height = Window.size
        min_dimension = min(width, height)
        
        if min_dimension >= ScreenConfig.TABLET_WIDTH:
            return 'tablet'
        elif min_dimension >= ScreenConfig.PHONE_WIDTH:
            return 'phone'
        else:
            return 'small_phone'
    
    @staticmethod
    def get_optimal_orientation():
        """
        Get optimal orientation for current screen size.
        
        Returns:
            str: 'horizontal' or 'vertical'
        """
        size_category = ScreenConfig.get_screen_size_category()
        orientation = ScreenConfig.get_screen_orientation()
        
        # Large screens (tablets) work well in both orientations
        if size_category == 'tablet':
            return 'horizontal' if orientation == 'landscape' else 'vertical'
        
        # Phones: landscape mode provides more horizontal space
        if size_category in ['phone', 'small_phone']:
            # Force horizontal layout for better game experience
            return 'horizontal'
        
        return 'vertical'
    
    @staticmethod
    def scale_font_size(base_size):
        """
        Scale font size based on screen size.
        
        Args:
            base_size: Base font size in sp
            
        Returns:
            float: Scaled font size
        """
        width, height = Window.size
        min_dimension = min(width, height)
        
        # Base reference: 360px (typical phone width)
        scale_factor = min_dimension / 360.0
        
        # Limit scale between 0.8 and 1.5
        scale_factor = max(0.8, min(1.5, scale_factor))
        
        return base_size * scale_factor
    
    @staticmethod
    def scale_spacing(base_spacing):
        """
        Scale spacing based on screen size.
        
        Args:
            base_spacing: Base spacing in sp
            
        Returns:
            float: Scaled spacing
        """
        return ScreenConfig.scale_font_size(base_spacing)
    
    @staticmethod
    def log_screen_info():
        """Log current screen information."""
        width, height = Window.size
        orientation = ScreenConfig.get_screen_orientation()
        size_category = ScreenConfig.get_screen_size_category()
        optimal = ScreenConfig.get_optimal_orientation()
        
        Logger.info(f"ScreenConfig:")
        Logger.info(f"  Size: {width}x{height}")
        Logger.info(f"  Orientation: {orientation}")
        Logger.info(f"  Category: {size_category}")
        Logger.info(f"  Optimal layout: {optimal}")


# Bind to window size changes to detect orientation changes
def _on_window_size(instance, value):
    """Handle window size changes."""
    ScreenConfig.log_screen_info()

Window.bind(size=_on_window_size)