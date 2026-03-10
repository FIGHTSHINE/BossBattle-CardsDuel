"""Main menu theme configuration."""
from utils.screen_config import ScreenConfig

class MenuTheme:
    """Centralized theme configuration for main menu."""
    
    # ============ Button Colors ============
    COLOR_BOSS_DUEL = (0.2, 0.7, 0.3, 1)    # Green - working mode
    COLOR_SURVIVAL = (0.4, 0.4, 0.4, 1)     # Gray - coming soon
    COLOR_PVP = (0.4, 0.4, 0.4, 1)          # Gray - coming soon
    COLOR_LANGUAGE = (0.3, 0.5, 0.9, 1)     # Blue
    COLOR_ABOUT = (0.6, 0.3, 0.8, 1)        # Purple
    COLOR_EXIT = (0.8, 0.3, 0.3, 1)         # Red
    
    # Mute button colors
    COLOR_MUTE_OFF = (0.2, 0.2, 0.2, 0.5)   # Semi-transparent dark
    COLOR_MUTE_ON = (0.8, 0.3, 0.3, 0.8)    # Red - when muted
    
    # Popup colors
    COLOR_POPUP_BG = (0.1, 0.1, 0.15, 0.9)  # Dark blue-gray background
    COLOR_POPUP_OVERLAY = (0, 0, 0, 0.6)    # Semi-transparent outer overlay
    COLOR_POPUP_BORDER = (0.3, 0.6, 1.0, 0.6)
    COLOR_RULES_TITLE = (0.3, 0.8, 1, 1)    # Bright cyan
    COLOR_RULES_TEXT = (0.95, 0.95, 0.95, 1)  # White/light gray
    COLOR_POPUP_BACK_BTN = (0.4, 0.4, 0.5, 1)  # Darker gray
    COLOR_POPUP_CONFIRM_BTN = (0.1, 0.7, 0.3, 1)  # Brighter green
    
    # ============ Font Sizes (Converted to Methods) ============
    @staticmethod
    def font_size_title():
        return ScreenConfig.scale_font_size(40)
    
    @staticmethod
    def font_size_mode_label():
        return ScreenConfig.scale_font_size(22)
    
    @staticmethod
    def font_size_boss_duel():
        return ScreenConfig.scale_font_size(26)
    
    @staticmethod
    def font_size_other_modes():
        return ScreenConfig.scale_font_size(20)
    
    @staticmethod
    def font_size_options_label():
        return ScreenConfig.scale_font_size(18)
    
    @staticmethod
    def font_size_options_btn():
        return ScreenConfig.scale_font_size(18)
    
    @staticmethod
    def font_size_lang_indicator():
        return ScreenConfig.scale_font_size(14)
    
    @staticmethod
    def font_size_mute():
        return ScreenConfig.scale_font_size(35)
    
    # Popup font sizes
    @staticmethod
    def font_size_popup_title():
        return ScreenConfig.scale_font_size(24)
    
    @staticmethod
    def font_size_rules_text():
        return ScreenConfig.scale_font_size(16)
    
    @staticmethod
    def font_size_popup_btn():
        return ScreenConfig.scale_font_size(18)
    
    @staticmethod
    def font_size_about_title():
        return ScreenConfig.scale_font_size(24)
    
    @staticmethod
    def font_size_about_content():
        return ScreenConfig.scale_font_size(16)
    
    @staticmethod
    def font_size_about_btn():
        return ScreenConfig.scale_font_size(18)
    
    # ============ Size Hints (Keep as-is - already proportional) ============
    SIZE_HINT_TITLE = 0.15
    SIZE_HINT_MODE_LABEL = 0.05
    SIZE_HINT_BOSS_DUEL = 0.15
    SIZE_HINT_OTHER_MODES = 0.12
    SIZE_HINT_SPACER = 0.05
    SIZE_HINT_OPTIONS_LABEL = 0.04
    SIZE_HINT_OPTIONS_BTN = 0.10
    SIZE_HINT_LANG_INDICATOR = 0.04
    
    # Popup size hints
    SIZE_HINT_RULES_TITLE = 0.12
    SIZE_HINT_RULES_TEXT = 0.53
    SIZE_HINT_RULES_BUTTONS = 0.25
    SIZE_HINT_ABOUT_CONTENT = 0.5
    SIZE_HINT_ABOUT_BTN = 0.2
    
    # ============ Text Colors ============
    COLOR_TITLE = (0.2, 0.6, 1, 1)          # Blue title
    COLOR_MODE_LABEL = (0.8, 0.8, 0.8, 1)   # Light gray
    COLOR_OPTIONS_LABEL = (0.7, 0.7, 0.7, 1)  # Medium gray
    COLOR_LANG_INDICATOR = (0.5, 0.5, 0.5, 1)  # Dark gray
    
    # ============ Popup Dimensions ============
    POPUP_RULES_SIZE = (0.85, 0.75)
    POPUP_ABOUT_SIZE = (0.8, 0.7)
    POPUP_BORDER_RADIUS = [20, 20, 20, 20]  # Rounded corners
    
    # ============ Mute Button (Convert to Method) ============
    @staticmethod
    def mute_btn_size():
        size = ScreenConfig.scale_spacing(60)
        return (size, size)
    
    MUTE_BTN_POS_HINT = {'right': 0.95, 'top': 0.95}
    
    # ============ Layout Spacing (Convert to Methods) ============
    @staticmethod
    def padding():
        return ScreenConfig.scale_spacing(20)
    
    @staticmethod
    def spacing():
        return ScreenConfig.scale_spacing(10)
    
    @staticmethod
    def popup_padding():
        return ScreenConfig.scale_spacing(25)
    
    @staticmethod
    def popup_spacing():
        return ScreenConfig.scale_spacing(15)
    
    @staticmethod
    def popup_button_spacing():
        return ScreenConfig.scale_spacing(10)
    
    # ============ Text Alignment ============
    # Main menu
    TITLE_HALIGN = 'center'
    TITLE_VALIGN = 'middle'
    MODE_LABEL_HALIGN = 'center'
    MODE_LABEL_VALIGN = 'middle'
    
    # Popup
    RULES_TEXT_HALIGN = 'left'
    RULES_TEXT_VALIGN = 'middle'
    ABOUT_CONTENT_HALIGN = 'center'
    ABOUT_CONTENT_VALIGN = 'middle'
    
    # ============ Text Size Multipliers ============
    RULES_TEXT_WIDTH_RATIO = 0.75  # Window.width * 0.75
    ABOUT_CONTENT_WIDTH_RATIO = 0.8  # Window.width * 0.8