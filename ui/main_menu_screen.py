"""Main menu screen."""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window

from game.translations import t, language_manager
from ui.font_config import get_chinese_font_name


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
        self.padding = '30sp'
        self.spacing = '12sp'
        
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
        """Build the main menu UI."""
        # Main title
        title = Label(
            text=t('MENU_TITLE'),
            font_size='40sp',
            size_hint_y=0.15,
            color=(0.2, 0.6, 1, 1),
            bold=True,
            font_name=self.chinese_font or 'Roboto',
            halign='center',
            valign='middle'
        )
        self.add_widget(title)
        
        # Game mode selection section
        mode_label = Label(
            text=t('MENU_SELECT_MODE'),
            font_size='22sp',
            size_hint_y=0.05,
            color=(0.8, 0.8, 0.8, 1),
            bold=True,
            font_name=self.chinese_font or 'Roboto'
        )
        self.add_widget(mode_label)
        
        # Boss Duel button (working mode - green)
        boss_duel_btn = Button(
            text=t('MENU_MODE_BOSS_DUEL'),
            font_size='26sp',
            size_hint_y=0.15,
            bold=True,
            background_color=(0.2, 0.7, 0.3, 1),  # Green
            font_name=self.chinese_font or 'Roboto'
        )
        boss_duel_btn.bind(on_press=lambda instance: self._on_mode_selected('boss_duel'))
        self.add_widget(boss_duel_btn)
        
        # Survival Mode (coming soon - grayed out)
        survival_btn = Button(
            text=t('MENU_MODE_SURVIVAL'),
            font_size='20sp',
            size_hint_y=0.12,
            background_color=(0.4, 0.4, 0.4, 1),  # Gray
            font_name=self.chinese_font or 'Roboto',
            disabled=True
        )
        self.add_widget(survival_btn)
        
        # PvP Mode (coming soon - grayed out)
        pvp_btn = Button(
            text=t('MENU_MODE_PVP'),
            font_size='20sp',
            size_hint_y=0.12,
            background_color=(0.4, 0.4, 0.4, 1),  # Gray
            font_name=self.chinese_font or 'Roboto',
            disabled=True
        )
        self.add_widget(pvp_btn)
        
        # Spacer
        spacer = Label(
            text='',
            size_hint_y=0.05
        )
        self.add_widget(spacer)
        
        # Options label
        options_label = Label(
            text=t('MENU_OPTIONS'),
            font_size='18sp',
            size_hint_y=0.04,
            color=(0.7, 0.7, 0.7, 1),
            font_name=self.chinese_font or 'Roboto'
        )
        self.add_widget(options_label)
        
        # Language button (blue)
        lang_btn = Button(
            text=t('MENU_LANGUAGE'),
            font_size='18sp',
            size_hint_y=0.10,
            background_color=(0.3, 0.5, 0.9, 1),  # Blue
            font_name=self.chinese_font or 'Roboto'
        )
        lang_btn.bind(on_press=lambda i: self._callback(self.on_language))
        self.add_widget(lang_btn)
        
        # About button (purple)
        about_btn = Button(
            text=t('MENU_ABOUT'),
            font_size='18sp',
            size_hint_y=0.10,
            background_color=(0.6, 0.3, 0.8, 1),  # Purple
            font_name=self.chinese_font or 'Roboto'
        )
        about_btn.bind(on_press=lambda i: self._callback(self.on_about))
        self.add_widget(about_btn)
        
        # Exit button (red)
        exit_btn = Button(
            text=t('MENU_EXIT'),
            font_size='18sp',
            size_hint_y=0.10,
            background_color=(0.8, 0.3, 0.3, 1),  # Red
            font_name=self.chinese_font or 'Roboto'
        )
        exit_btn.bind(on_press=lambda i: self._callback(self.on_exit))
        self.add_widget(exit_btn)
        
        # Language indicator
        lang_indicator = Label(
            text=f"Language: {language_manager.current_language.upper()} | 语言: {language_manager.current_language.upper()}",
            font_size='14sp',
            size_hint_y=0.04,
            color=(0.5, 0.5, 0.5, 1),
            font_name=self.chinese_font or 'Roboto'
        )
        self.add_widget(lang_indicator)
    
    def _on_mode_selected(self, mode):
        """Handle game mode selection."""
        try:
            print(f"[MainMenu] _on_mode_selected called with mode: {mode}")
            print(f"[MainMenu] self.on_start_game: {self.on_start_game}")
            
            if self.on_start_game:
                print(f"[MainMenu] Calling on_start_game...")
                self.on_start_game(mode)
                print(f"[MainMenu] on_start_game completed")
            else:
                print(f"[MainMenu] Warning: on_start_game is None")
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
            print(f"[MainMenu] refresh_text called")
            self.clear_widgets()
            self.build_ui()
            print(f"[MainMenu] refresh_text completed")
        except Exception as e:
            print(f"[MainMenu] ❌ Error in refresh_text: {e}")
            import traceback
            traceback.print_exc()

    def show_about_popup(self):
        """Show about popup dialog."""
        try:
            print(f"[MainMenu] show_about_popup called")
            about_content = BoxLayout(orientation='vertical', padding='20sp', spacing='10sp')
            
            title_label = Label(
                text=t('MENU_ABOUT_TITLE'),
                font_size='24sp',
                bold=True,
                font_name=self.chinese_font or 'Roboto'
            )
            
            content_label = Label(
                text=t('MENU_ABOUT_CONTENT'),
                font_size='16sp',
                size_hint_y=0.5,
                font_name=self.chinese_font or 'Roboto',
                halign='center',
                valign='middle',
                text_size=(Window.width * 0.8, None)
            )
            
            close_btn = Button(
                text='OK',
                font_size='18sp',
                size_hint_y=0.2,
                background_color=(0.5, 0.5, 0.5, 1),
                font_name=self.chinese_font or 'Roboto'
            )
            
            about_content.add_widget(title_label)
            about_content.add_widget(content_label)
            about_content.add_widget(close_btn)
            
            popup = Popup(
                title='About',
                content=about_content,
                size_hint=(0.8, 0.7),
                auto_dismiss=False
            )
            
            close_btn.bind(on_press=popup.dismiss)
            popup.open()
            print(f"[MainMenu] show_about_popup completed")
        except Exception as e:
            print(f"[MainMenu] ❌ Error in show_about_popup: {e}")
            import traceback
            traceback.print_exc()