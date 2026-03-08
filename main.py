"""Boss Battle Card Game - Main Entry Point."""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform  # ✅ 添加导入

from ui.language_select_screen import LanguageSelectScreen
from ui.main_menu_screen import MainMenuScreen
from ui.game_screen import GameScreen
from ui.font_config import init_fonts  # ✅ 修改导入


class BossBattleApp(App):
    """Main application class."""
    
    def __init__(self, **kwargs):
        """Initialize the application."""
        super().__init__(**kwargs)
        self.game_screen = None
        self.main_menu = None
        
        # ✅ 不要在 __init__ 中注册字体
        # 改为在 build() 中注册
        pass
    
    def build(self):
        """Build and return the root widget."""
        self.title = "Boss Battle - 卡牌战斗"
        
        # ✅ 在 build() 中注册字体（更安全）
        init_fonts()
        
        # Start with language selection screen
        lang_screen = LanguageSelectScreen(self.on_language_selected)
        return lang_screen
    
    def on_language_selected(self, lang_code):
        """
        Callback when language is selected.
        
        Args:
            lang_code: 'zh' or 'en'
        """
        print(f"[App] Language selected: {lang_code}")
        
        # Clear language screen and show MAIN MENU
        self.root.clear_widgets()
        self.main_menu = MainMenuScreen(
            on_start_game=self.on_start_game,
            on_language=self.on_change_language,
            on_about=self.on_about,
            on_exit=self.on_exit
        )
        self.root.add_widget(self.main_menu)
    
    def on_start_game(self, mode):
        """
        Start a new game in the selected mode.
        
        Args:
            mode: Game mode ('boss_duel', 'survival', 'pvp', etc.)
        """
        import traceback
        import sys
        
        print(f"[App] Starting game mode: {mode}")
        
        try:
            # Currently only 'boss_duel' mode is implemented
            if mode == 'boss_duel':
                print("[App] Clearing root widgets...")
                self.root.clear_widgets()
                
                print("[App] Creating GameScreen...")
                print(f"[App] Python version: {sys.version}")
                print(f"[App] Platform: {platform}")
                
                self.game_screen = GameScreen(on_back_to_menu=self.on_back_to_menu)
                print("[App] GameScreen created successfully")
                
                print("[App] Adding game screen to root...")
                self.root.add_widget(self.game_screen)
                print("[App] Game screen added successfully")
            else:
                print(f"[App] Game mode '{mode}' not implemented yet")
        
        except Exception as e:
            print(f"[APP ERROR] Failed to start game: {str(e)}")
            print(f"[APP ERROR] Error type: {type(e).__name__}")
            print(f"[APP ERROR] Traceback:\n{traceback.format_exc()}")
            
            # 尝试恢复到主菜单
            try:
                if self.root:
                    self.root.clear_widgets()
                    if self.main_menu:
                        self.root.add_widget(self.main_menu)
            except:
                print("[APP ERROR] Failed to recover to main menu")
    
    def on_change_language(self, instance):
        """Toggle language and refresh the menu."""
        import traceback
        
        try:
            from game.translations import language_manager
            
            # Toggle language
            new_lang = 'en' if language_manager.current_language == 'zh' else 'zh'
            language_manager.set_language(new_lang)
            
            print(f"[App] Language changed to: {new_lang}")
            
            # Refresh menu to update translations
            if self.main_menu:
                self.main_menu.refresh_text()
        
        except Exception as e:
            print(f"[APP ERROR] Failed to change language: {str(e)}")
            print(f"[APP ERROR] Traceback:\n{traceback.format_exc()}")
    
    def on_about(self, instance):
        """Show about dialog."""
        import traceback
        
        try:
            if self.main_menu:
                self.main_menu.show_about_popup()
        
        except Exception as e:
            print(f"[APP ERROR] Failed to show about: {str(e)}")
            print(f"[APP ERROR] Traceback:\n{traceback.format_exc()}")
    
    def on_exit(self, instance):
        """Exit the application."""
        import traceback
        
        try:
            print("[App] Exiting application...")
            App.get_running_app().stop()
        
        except Exception as e:
            print(f"[APP ERROR] Failed to exit: {str(e)}")
            print(f"[APP ERROR] Traceback:\n{traceback.format_exc()}")
    
    def on_back_to_menu(self):
        """Return to main menu from game screen."""
        print("[App] Returning to main menu...")
    
        # Clear game screen
        self.root.clear_widgets()
        self.game_screen = None
        
        # Rebuild and show main menu
        self.main_menu = MainMenuScreen(
            on_start_game=self.on_start_game,
            on_language=self.on_change_language,
            on_about=self.on_about,
            on_exit=self.on_exit
        )
        self.root.add_widget(self.main_menu)

if __name__ == '__main__':
    BossBattleApp().run()