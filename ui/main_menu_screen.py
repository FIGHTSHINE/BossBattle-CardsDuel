"""Main menu screen."""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.app import App  # ✅ 添加这一行
from kivy.graphics import Color, Rectangle, RoundedRectangle
from ui.menu_builders import MenuTheme
from ui.menu_builders import PopupFactory
from game.translations import t, language_manager
from ui.font_config import get_chinese_font_name
from utils.screen_config import ScreenConfig
from ui.menu_builders import TitleBuilder
from ui.menu_builders import ModeSectionBuilder
from ui.menu_builders import OptionsSectionBuilder
from ui.menu_builders import MuteButtonBuilder

class MainMenuScreen(BoxLayout):
    """Main menu screen with game mode selection."""
    
    def __init__(self, on_start_game=None, on_language=None, 
                 on_about=None, on_exit=None, **kwargs):
        """
        Initialize main menu screen.
        
        Args:
            on_start_game: Callback when game mode selected (receives mode string)
            on_language: Callback for language button
            on_about: Callback for about button
            on_exit: Callback for exit button
        """
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = ScreenConfig.scale_padding(20)
        self.spacing = ScreenConfig.scale_spacing(10)
        
        self.on_start_game = on_start_game
        self.on_language = on_language
        self.on_about = on_about
        self.on_exit = on_exit
        
        # ✅ 添加强制保护：确保字体名称不为 None
        self.chinese_font = get_chinese_font_name()
        if self.chinese_font is None:
            print("[MainMenu] ⚠️ WARNING: get_chinese_font_name() returned None, using 'Roboto'")
            self.chinese_font = 'Roboto'
        
        print(f"[MainMenu] Using font: {self.chinese_font}")
        self.build_ui()
    
    def build_ui(self):
        """Build the main menu UI using modular builders."""
        # Title section
        title = TitleBuilder.build(self.chinese_font)
        self.add_widget(title)
        
        # Game mode selection section
        mode_widgets = ModeSectionBuilder.build(
            self.chinese_font,
            self._on_mode_selected
        )
        for widget in mode_widgets:
            self.add_widget(widget)
        
        # Options section
        option_widgets = OptionsSectionBuilder.build(
            self.chinese_font,
            lambda: self._callback(self.on_language),
            lambda: self._callback(self.on_about),
            lambda: self._callback(self.on_exit)
        )
        for widget in option_widgets:
            self.add_widget(widget)
        
        # Mute button
        mute_btn = MuteButtonBuilder.build(
            self.chinese_font,
            self._toggle_mute
        )
        self.add_widget(mute_btn)
        self.mute_button = mute_btn
    
    def _on_mode_selected(self, mode):
        """
        Handle game mode selection.
        
        Shows rules popup first, then waits for user confirmation.
        
        Args:
            mode: Game mode string ('boss_duel', 'survival', 'pvp')
        """
        try:
            print(f"[MainMenu] _on_mode_selected called with mode: {mode}")
            
            # Show rules popup instead of directly starting game
            self._show_mode_rules_popup(mode)
            
        except Exception as e:
            print(f"[MainMenu] ❌ Error in _on_mode_selected: {e}")
            import traceback
            traceback.print_exc()

    def _callback(self, callback):
        """Execute callback if provided."""
        try:
            print(f"[MainMenu] _callback called with callback: {callback}")
            if callback:
                print(f"[MainMenu] Executing callback...")
                callback(instance=None)
                print(f"[MainMenu] Callback completed")
        except Exception as e:
            print(f"[MainMenu] ❌ Error in _callback: {e}")
            import traceback
            traceback.print_exc()

    def refresh_text(self):
        """Refresh all button texts after language change."""
        try:
            # ✅ 添加：重新计算 padding 和 spacing
            from utils.screen_config import ScreenConfig
            self.padding = ScreenConfig.scale_spacing(20)
            self.spacing = ScreenConfig.scale_spacing(10)

            print(f"[MainMenu] refresh_text called")
            self.clear_widgets()
            self.build_ui()
            print(f"[MainMenu] refresh_text completed")
        except Exception as e:
            print(f"[MainMenu] ❌ Error in refresh_text: {e}")
            import traceback
            traceback.print_exc()

    def show_about_popup(self):
        """Show about popup."""
        popup = PopupFactory.create_about_popup(self.chinese_font)
        popup.open()

    def _toggle_mute(self, instance):
        """Toggle mute button callback."""
        app = App.get_running_app()
        is_muted = app.audio_manager.toggle_mute()
    
        # Update button text and color
        if is_muted:
            instance.text = t('UI_MUTE_ON')  # "静音" / "Mute"
            instance.background_color = (0.8, 0.3, 0.3, 0.8)
        else:
            instance.text = t('UI_MUTE_OFF')  # "声音" / "Sound"
            instance.background_color = (0.3, 0.8, 0.3, 0.8)

    def _show_mode_rules_popup(self, mode):
        """
        Show game mode rules confirmation popup.
        
        Args:
            mode: Game mode string ('boss_duel', 'survival', 'pvp')
        """
        try:
            popup = PopupFactory.create_rules_popup(
                mode, 
                self.chinese_font, 
                lambda: self._confirm_start_game(mode, popup)
            )
            popup.open()
            
        except Exception as e:
            print(f"[MainMenu] ❌ Error in _show_mode_rules_popup: {e}")
            import traceback
            traceback.print_exc()
    
    def _confirm_start_game(self, mode, popup):
        """
        Confirm and start game after rules confirmation.
        
        Args:
            mode: Game mode string
            popup: Popup instance to dismiss
        """
        try:
            print(f"[MainMenu] _confirm_start_game called with mode: {mode}")
            
            # Dismiss popup first
            popup.dismiss()
            
            # Start the game
            if self.on_start_game:
                print(f"[MainMenu] Starting game mode: {mode}")
                self.on_start_game(mode)
            else:
                print(f"[MainMenu] Warning: on_start_game is None")
                
        except Exception as e:
            print(f"[MainMenu] ❌ Error in _confirm_start_game: {e}")
            import traceback
            traceback.print_exc()
