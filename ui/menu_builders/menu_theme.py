"""Main menu theme configuration."""

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
    
    # ============ Font Sizes ============
    FONT_SIZE_TITLE = '40sp'
    FONT_SIZE_MODE_LABEL = '22sp'
    FONT_SIZE_BOSS_DUEL = '26sp'
    FONT_SIZE_OTHER_MODES = '20sp'
    FONT_SIZE_OPTIONS_LABEL = '18sp'
    FONT_SIZE_OPTIONS_BTN = '18sp'
    FONT_SIZE_LANG_INDICATOR = '14sp'
    FONT_SIZE_MUTE = '35sp'
    
    # Popup font sizes
    FONT_SIZE_POPUP_TITLE = '24sp'
    FONT_SIZE_RULES_TEXT = '16sp'
    FONT_SIZE_POPUP_BTN = '18sp'
    FONT_SIZE_ABOUT_TITLE = '24sp'
    FONT_SIZE_ABOUT_CONTENT = '16sp'
    FONT_SIZE_ABOUT_BTN = '18sp'
    
    # ============ Size Hints ============
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
    POPUP_BORDER_RADIUS = [20, 20, 20, 20]  # Rounded corners (20sp)
    
    # ============ Mute Button ============
    MUTE_BTN_SIZE = ('60sp', '60sp')
    MUTE_BTN_POS_HINT = {'right': 0.95, 'top': 0.95}
    
    # ============ Layout Spacing ============
    PADDING = '20sp'
    SPACING = '10sp'
    POPUP_PADDING = '25sp'
    POPUP_SPACING = '15sp'
    POPUP_BUTTON_SPACING = '10sp'
    
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