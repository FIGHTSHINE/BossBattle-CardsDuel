"""Screen configuration and responsive layout utilities."""

from kivy.core.window import Window
from kivy.logger import Logger
from kivy.metrics import Metrics


class ScreenConfig:
    """Manage screen configuration and responsive layouts."""
    
    # Screen size breakpoints
    TABLET_WIDTH = 600  # pixels
    PHONE_WIDTH = 360   # pixels
    
    _last_scale_factor = None
    
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
    def scale_height(base_height):
        """
        Scale widget height based on screen size.

        Args:
            base_height: Base height value in sp

        Returns:
            float: Scaled height
        """
        return ScreenConfig.scale_spacing(base_height)

    @staticmethod
    def scale_width(base_width):
        """
        Scale widget width based on screen size.

        Args:
            base_width: Base width value in sp

        Returns:
            float: Scaled width
        """
        return ScreenConfig.scale_spacing(base_width)

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
        # min_dimension = min(width, height)
        
        # Base reference: 1280px (typical desktop width)
        scale_factor = width / 1280.0
        
        # Limit scale between 0.8 and 1.5
        scale_factor = max(0.8, min(1.5, scale_factor))
        
        return base_size * scale_factor

    @staticmethod
    def get_markup_size(base_size):
        """
        Get font size formatted for Kivy markup text.

        This is useful for game messages that use markup like "[size=24]text[/size]".

        Args:
            base_size: Base font size in sp

        Returns:
            str: Formatted size tag for markup (e.g., "[size=24.5]")
        """
        scaled_size = ScreenConfig.scale_font_size(base_size)
        return f"[size={int(scaled_size)}]"    

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
    def scale_padding(base_padding):
        """
        Scale padding based on screen size.

        Args:
            base_padding: Base padding value in sp

        Returns:
            float: Scaled padding
        """
        # Padding和spacing使用相同的缩放策略
        return ScreenConfig.scale_spacing(base_padding)
    
    @staticmethod
    def get_layout_ratios():
        """
        Get layout size_hint ratios based on device category.
        
        Returns:
            dict: Dictionary containing size_hint values for different components
        """
        size_category = ScreenConfig.get_screen_size_category()
        
        # Default ratios (current layout)
        ratios = {
            'boss_area': 0.2,      # Boss widget area
            'player_area': 0.25,   # Player widget area
            'battle_area': 0.18,   # Battle messages area
            'turn_counter': 0.05,  # Turn counter
            'turn_indicator': 0.08, # Turn indicator
            'shield_label': 0.04,  # Shield value
            'cards_info': 0.04,    # Deck/hand counts
            'cards_played': 0.04,  # Turn card counter
            'end_turn_btn': 0.08,  # End turn button
            'stats_area': 0.5,     # Stats display (top half)
            'hand_area': 0.5,      # Hand display (bottom half)
        }
        
        # Optional: Adjust ratios for tablets if needed
        # Currently maintaining same proportions across all devices
        # Uncomment below to customize tablet layout:
        # if size_category == 'tablet':
        #     ratios['boss_area'] = 0.15
        #     ratios['player_area'] = 0.2
        #     ratios['battle_area'] = 0.15
        
        return ratios
    
    
    @staticmethod
    def calculate_card_size():
        """
        Calculate card dimensions based on screen width.
        
        Maintains aspect ratio of 1.4:1 (140:100)
        
        Returns:
            tuple: (width, height) in pixels
        """
        width, height = Window.size
        size_category = ScreenConfig.get_screen_size_category()
        
        # Base card size (reference: 140x100 pixels)
        base_card_width = 140
        base_card_height = 100
        aspect_ratio = base_card_width / base_card_height  # 1.4
        
        # Calculate scale factor based on screen width
        # Reference width: 1280px (typical landscape phone)
        reference_width = 1280
        scale_factor = width / reference_width
        
        # Limit scale between 0.7 and 1.3 for usability
        scale_factor = max(0.7, min(1.3, scale_factor))
        
        # Adjust for tablets (can be slightly larger)
        if size_category == 'tablet':
            scale_factor = min(scale_factor, 1.2)
        
        card_width = base_card_width * scale_factor
        card_height = card_width / aspect_ratio
        
        return (card_width, card_height)
    @staticmethod
    def calculate_boss_size():
        """
        Calculate boss widget dimensions based on screen width.

        Boss icon should be proportional to card size for visual consistency.

        Returns:
            tuple: (width, height) in pixels
        """
        width, height = Window.size
        size_category = ScreenConfig.get_screen_size_category()

        # Base boss size (reference: 100x100 pixels)
        base_boss_size = 100

        # Calculate scale factor based on screen width
        reference_width = 1280
        scale_factor = width / reference_width

        # Limit scale between 0.7 and 1.3 for usability
        scale_factor = max(0.7, min(1.3, scale_factor))

        # Adjust for tablets
        if size_category == 'tablet':
            scale_factor = min(scale_factor, 1.2)

        boss_size = base_boss_size * scale_factor

        return (boss_size, boss_size)   


    @staticmethod
    def calculate_player_size():
        """
        Calculate player widget dimensions based on screen width.

        Player icon should be slightly smaller than boss for visual hierarchy.

        Returns:
            tuple: (width, height) in pixels
        """
        width, height = Window.size
        size_category = ScreenConfig.get_screen_size_category()

        # Base player size (reference: 80x80 pixels, smaller than boss)
        base_player_size = 80

        # Calculate scale factor based on screen width
        reference_width = 1280
        scale_factor = width / reference_width

        # Limit scale between 0.7 and 1.3 for usability
        scale_factor = max(0.7, min(1.3, scale_factor))

        # Adjust for tablets
        if size_category == 'tablet':
            scale_factor = min(scale_factor, 1.2)

        player_size = base_player_size * scale_factor

        return (player_size, player_size)
    
    @staticmethod
    def get_optimal_spacing(base_spacing):
        """
        Get optimal spacing value based on screen size.
        
        This is an alias for scale_spacing() for consistent naming.
        
        Args:
            base_spacing: Base spacing in sp
            
        Returns:
            float: Scaled spacing
        """
        return ScreenConfig.scale_spacing(base_spacing)
    
    # In ScreenConfig class, add:

    @staticmethod
    def has_scale_changed():
        """
        Check if screen scale has changed significantly.
        
        Returns:
            bool: True if scale changed by more than 5%
        """
        width, height = Window.size
        min_dimension = min(width, height)
        current_scale = min_dimension / 360.0
        
        if ScreenConfig._last_scale_factor is None:
            ScreenConfig._last_scale_factor = current_scale
            return False
        
        # Check for more than 5% change
        change_percent = abs(current_scale - ScreenConfig._last_scale_factor) / ScreenConfig._last_scale_factor
        ScreenConfig._last_scale_factor = current_scale
        
        return change_percent > 0.05


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