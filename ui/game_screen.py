"""Main game screen UI - Refactored coordinator pattern."""

from kivy.uix.boxlayout import BoxLayout
from ui.font_config import get_chinese_font_name
from game.game_controller import GameController
from ui.ui_logger import UILogger
from ui.ui_builder import UIBuilder
from ui.hand_display import HandDisplay
from ui.stats_display import StatsDisplay
from ui.game_managers import GameAnimationManager, GameFlowManager, GameButtonManager
from ui.turn_event_handler import TurnEventHandler
from game.models import CardType
from game.translations import Translations as T


class GameScreen(BoxLayout):
    """
    Main game screen - coordinator pattern implementation.
    
    This is a coordinator that delegates to specialized managers:
    - GameAnimationManager: Handles all animations
    - GameFlowManager: Manages game flow and end-game scenarios
    - GameButtonManager: Manages button creation and events
    - TurnEventHandler: Handles turn-based events
    """
    
    def __init__(self, on_back_to_menu):
        """Initialize the game screen and all managers."""
        import traceback
        
        print("[GameScreen] Initializing...")
        
        try:
            super().__init__()
            print("[GameScreen] Super init complete")
            
            self.orientation = 'vertical'
            self.padding = '20sp'
            self.spacing = '10sp'
            print("[GameScreen] Layout properties set")
            
            # Store callback
            self.on_back_to_menu = on_back_to_menu
            
            # Initialize controller
            print("[GameScreen] Creating GameController...")
            self.controller = GameController()
            print("[GameScreen] GameController created")
            
            # Initialize UI components
            print("[GameScreen] Creating UIBuilder...")
            self.builder = UIBuilder(self)
            print("[GameScreen] UIBuilder created")
            
            print("[GameScreen] Creating StatsDisplay...")
            self.stats_display = StatsDisplay()
            print("[GameScreen] StatsDisplay created")
            
            print("[GameScreen] Creating HandDisplay...")
            self.hand_display = HandDisplay(self.on_card_play)
            print("[GameScreen] HandDisplay created")
            
            # ✅ 正确的初始化顺序：
            print("[GameScreen] Creating subsystem managers...")
            self.animation_manager = GameAnimationManager(self.stats_display)

            # ✅ 先创建 button_manager
            self.button_manager = GameButtonManager(self)

            # ✅ 再创建 flow_manager（此时 button_manager 已经存在）
            self.flow_manager = GameFlowManager(
                self.controller, 
                self.stats_display, 
                self.animation_manager,
                button_manager=self.button_manager,  # ✅ 现在 self.button_manager 已经创建
                game_screen=self                     
            )
            self.turn_handler = TurnEventHandler(self.controller, self)
            print("[GameScreen] All managers created")
            
            # Build UI
            print("[GameScreen] Building UI...")
            UILogger.log_ui_build_start()
            self.build_ui()
            UILogger.log_init_success()
            print("[GameScreen] UI build complete")
            
        except Exception as e:
            print(f"[GameScreen ERROR] Initialization failed: {str(e)}")
            print(f"[GameScreen ERROR] Traceback:\n{traceback.format_exc()}")
            raise
    
    def build_ui(self):
        """Build the user interface."""
        # Build and add stats display
        self.stats_display.build_stats(self.builder)
        self.add_widget(self.stats_display)
        
        # Add end turn button separately
        self.stats_display.add_end_turn_button(self.on_end_turn)
        
        # Add hand display
        self.add_widget(self.hand_display)
        
        # Initial display
        self.refresh_display()
        
        UILogger.log_ui_build_complete()
    
    def refresh_display(self):
        """
        Refresh all displays from controller state.
        
        This method remains in GameScreen as it coordinates multiple components.
        """
        stats = self.controller.get_stats()
        hand = self.controller.get_hand()
        
        # Update stats
        self.stats_display.update_stats(stats)
        self.stats_display.update_turn_indicator(stats['is_player_turn'])
        self.stats_display.update_cards_played(
            self.controller.battle.cards_played_this_turn,
            self.controller.battle.max_cards_per_turn
        )
        
        # Update hand
        self.hand_display.display_hand(hand, self.builder)
    
    def on_card_play(self, card):
        """
        Handle card play event.
        
        Delegates to TurnEventHandler.
        
        Args:
            card: Card object to play
        """
        self.turn_handler.handle_card_play(card)
    
    def on_end_turn(self, instance):
        """
        Handle end turn button press.
        
        Delegates to TurnEventHandler.
        
        Args:
            instance: Button widget (unused)
        """
        self.turn_handler.handle_turn_end()
    
    def on_restart(self, instance):
        """
        Handle restart button press.

        Args:
            instance: Button widget (unused)
        """
        self.controller.reset()

        # ✅ Restart battle music for new game
        print("[GameScreen] Restarting battle music...")
        from kivy.app import App #type: ignore Import here to avoid circular import issues 
        App.get_running_app().audio_manager.play_battle_music(loop=True)
        print("[GameScreen] Battle music restarted")

        # Clear and rebuild
        self.clear_widgets()
        self.builder = UIBuilder(self)
        self.stats_display = StatsDisplay()
        self.hand_display = HandDisplay(self.on_card_play)

        # ✅ 正确的初始化顺序（与 __init__ 保持一致）
        self.animation_manager = GameAnimationManager(self.stats_display)
        self.button_manager = GameButtonManager(self)
        self.flow_manager = GameFlowManager(
            self.controller, 
            self.stats_display, 
            self.animation_manager,
            button_manager=self.button_manager,
            game_screen=self
        )
        self.turn_handler = TurnEventHandler(self.controller, self)

        self.build_ui()
    
    def on_back_to_menu_clicked(self, instance):
        """
        Handle return to main menu button press.
        
        Args:
            instance: Button widget (unused)
        """
        if self.on_back_to_menu:
            self.on_back_to_menu()
        else:
            print("[GameScreen] Warning: No callback provided for returning to menu")
    
    def get_card_color(self, card):
        """
        Get color based on card type.
        
        Args:
            card: Card object
            
        Returns:
            tuple: RGB color
        """
        if card.card_type == CardType.HEAL:
            return (0.2, 1, 0.5, 1)
        elif card.card_type == CardType.SHIELD:
            return (0.3, 0.7, 1, 1)
        elif card.card_type == CardType.CRITICAL:
            return (0.9, 0.3, 1, 1)
        else:
            return (0.9, 0.9, 0.9, 1)
