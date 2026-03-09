"""Boss Battle Card Game - Main Entry Point."""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import platform
from kivy.logger import Logger
from ui.language_select_screen import LanguageSelectScreen
from ui.main_menu_screen import MainMenuScreen
from ui.game_screen import GameScreen
from ui.font_config import init_fonts
from ui.audio_manager import AudioManager
from utils.sound_generator import SoundGenerator


class BossBattleApp(App):
    """Main application class."""
    
    def __init__(self, **kwargs):
        """Initialize the application."""
        super().__init__(**kwargs)
        self.game_screen = None
        self.main_menu = None
        self.audio_manager = AudioManager()
    
    def build(self):
        """Build and return the root widget."""
        self.title = "Boss Battle - 卡牌战斗"
        
        # # ✅ 测试横屏模式
        # if platform in ['win', 'macosx', 'linux']:
        #     # Set initial window size for testing (phone size in landscape)
        #     Window.size = (800, 480)  # Landscape mode
        #     Logger.info(f"App: Desktop mode - Testing landscape mode")
        # elif platform == 'android':
        #     # Android: 设置为横屏
        #     from jnius import autoclass # type: ignore
        #     PythonActivity = autoclass('org.kivy.android.PythonActivity')
        #     activity = PythonActivity.mActivity
        #     activity.setRequestedOrientation(0)  # 0 = LANDSCAPE
        #     Logger.info("App: Android - Forced landscape mode")
        
        # 注册字体
        init_fonts()
        
        # 初始化音频
        self._init_audio()
        
        # 语言选择界面
        lang_screen = LanguageSelectScreen(self.on_language_selected)
        return lang_screen
    
    def on_start(self):
        """Called when application starts."""
        Logger.info("App: Application started")
    
    def _init_audio(self):
        """Initialize audio system."""
        try:
            from utils.sound_generator import SoundGenerator
            
            Logger.info("App: Initializing audio system...")
            
            # Generate sound effects
            generator = SoundGenerator()
            
            # Generate all sounds
            victory_sound = generator.generate_victory_fanfare()
            defeat_sound = generator.generate_defeat_sound()
            card_play_sound = generator.generate_card_play_sound()  # ✅ 添加
            boss_attack_sound = generator.generate_boss_attack_sound()  # ✅ 添加
            menu_music = generator.generate_background_music_loop()  # ✅ 改名：menu_music
            battle_music = generator.generate_battle_music_loop()    # ✅ 新增：生成战斗音乐
            
            # Register sounds with audio manager
            self.audio_manager.set_sound_file('victory', victory_sound)
            self.audio_manager.set_sound_file('defeat', defeat_sound)
            self.audio_manager.set_sound_file('card_play', card_play_sound)  # ✅ 添加
            self.audio_manager.set_sound_file('boss_attack', boss_attack_sound)  # ✅ 添加
            self.audio_manager.set_sound_file('menu_music', menu_music)          # ✅ 改名：menu_music
            self.audio_manager.set_sound_file('battle_music', battle_music)     # ✅ 新增：注册战斗音乐
            
            # Load all sounds
            self.audio_manager.load_sounds()
            
            Logger.info("App: Audio system initialized successfully")
            
        except Exception as e:
            Logger.error(f"App: Failed to initialize audio: {e}")
            import traceback
            traceback.print_exc()
    
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
        
        # ✅ 启动菜单音乐
        self.audio_manager.play_menu_music(loop=True)
        print("[App] Menu music started")
    
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
                
                # ✅ Switch to battle music when game starts
                print("[App] Switching to battle music...")
                self.audio_manager.play_battle_music(loop=True)
                print("[App] Battle music started")
                
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

        # ✅ Switch back to menu music
        print("[App] Switching to menu music...")
        self.audio_manager.play_menu_music(loop=True)
        print("[App] Menu music started")

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