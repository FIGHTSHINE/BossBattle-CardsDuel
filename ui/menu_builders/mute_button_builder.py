"""Mute button builder for main menu."""

from kivy.uix.button import Button
from kivy.app import App
from game.translations import language_manager,t
from .menu_theme import MenuTheme


class MuteButtonBuilder:
    """Builder for mute button."""
    
    @staticmethod
    def build(font_name, on_toggle_mute):
        """
        Build mute button widget.
        
        Args:
            font_name: Font name to use
            on_toggle_mute: Callback when mute button released
        
        Returns:
            Button widget configured as mute button
        """
        # Get initial text and color based on current mute state
        mute_btn_text = t('UI_MUTE_OFF') if not App.get_running_app().audio_manager.muted else t('UI_MUTE_ON')
        
        mute_btn = Button(
            text=mute_btn_text,
            font_size=MenuTheme.font_size_mute(),
            size_hint=(None, None),
            size=MenuTheme.mute_btn_size(),
            pos_hint=MenuTheme.MUTE_BTN_POS_HINT,
            background_color=MenuTheme.COLOR_MUTE_OFF,
            font_name=font_name or 'Roboto',
            on_release=on_toggle_mute
        )
        
        # Set initial state if muted
        try:
            if App.get_running_app().audio_manager.muted:
                mute_btn.text = t('UI_MUTE_ON')
                mute_btn.background_color = MenuTheme.COLOR_MUTE_ON
        except:
            pass
        
        return mute_btn