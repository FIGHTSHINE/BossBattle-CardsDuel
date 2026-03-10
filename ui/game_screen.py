"""Main game screen UI - Refactored coordinator pattern."""

from kivy.uix.boxlayout import BoxLayout
# ✅ 新增导入（添加在第3行之后）
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
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
from utils.screen_config import ScreenConfig

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
            self.padding = ScreenConfig.scale_padding(20)
            self.spacing = ScreenConfig.scale_spacing(10)
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

            # ✅ 新增：创建特效覆盖层（不占用布局空间）
            print("[GameScreen] Creating effects overlay...")
            self.effects_overlay = FloatLayout(
                size_hint=(1, None),
                height=0  # 不参与 BoxLayout 空间分配
            )
            print("[GameScreen] Effects overlay created")

            self.build_ui()
            UILogger.log_init_success()
            print("[GameScreen] UI build complete")
            
        except Exception as e:
            print(f"[GameScreen ERROR] Initialization failed: {str(e)}")
            print(f"[GameScreen ERROR] Traceback:\n{traceback.format_exc()}")
            raise
    
    def build_ui(self):
        """
        Build the user interface.
        
        Structure (vertical BoxLayout):
        - StatsDisplay: Fixed UI (boss, player, HP, etc)
        - EffectsOverlay: FloatLayout for dynamic elements (fireballs, particles)
        - HandDisplay: Bottom card display area
        """
        # Build and add stats display (fixed UI at top)
        self.stats_display.build_stats(self.builder)
        self.add_widget(self.stats_display)
        
        # Add end turn button
        self.stats_display.add_end_turn_button(self.on_end_turn)
        
        # Add hand display at the bottom
        self.add_widget(self.hand_display)

        # ✅ 添加特效覆盖层（动态元素，不影响固定UI布局）
        self.add_widget(self.effects_overlay)
        
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
        # ✅ 新增：重建覆盖层（不占用布局空间）
        self.effects_overlay = FloatLayout(
            size_hint=(1, None),
            height=0  # 不参与 BoxLayout 空间分配
        )

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

    def refresh_ui(self):
        """
        Refresh all UI elements with current screen scaling.

        Preserves game state and re-adds game-over buttons if needed.
        """
        try:
            print("[GameScreen] Refreshing UI scaling...")

            # ✅ 检查游戏是否结束
            is_game_over = self.controller.is_game_over()
            game_result = None
            if is_game_over:
                # 保存游戏结果（胜利/失败）
                stats = self.controller.get_stats()
                if stats['boss_hp'] <= 0:
                    game_result = 'win'
                elif stats['player_hp'] <= 0:
                    game_result = 'lose'
                print(f"[GameScreen] Game is over, result: {game_result}")

            # ✅ 保存 effects_overlay 的子元素（如果有的话）
            overlay_children = []
            if hasattr(self, 'effects_overlay') and self.effects_overlay:
                overlay_children = list(self.effects_overlay.children)
                print(f"[GameScreen] Found {len(overlay_children)} children in effects_overlay")

            # Refresh padding and spacing
            self.padding = ScreenConfig.scale_padding(20)
            self.spacing = ScreenConfig.scale_spacing(10)

            # Refresh stats display if it exists
            if hasattr(self, 'stats_display') and self.stats_display:
                # Get current stats before rebuilding
                stats = self.controller.get_stats()

                # Remove old stats display
                self.remove_widget(self.stats_display)

                # Create new stats display
                self.stats_display = StatsDisplay()
                self.stats_display.build_stats(self.builder)
                self.add_widget(self.stats_display, index=0)  # Add at top

                # Update stats with current values
                self.stats_display.update_stats(stats)
                self.stats_display.update_turn_indicator(stats['is_player_turn'])
                self.stats_display.update_cards_played(
                    self.controller.battle.cards_played_this_turn,
                    self.controller.battle.max_cards_per_turn
                )

                # Re-add end turn button
                self.stats_display.add_end_turn_button(self.on_end_turn)

            # Refresh hand display if it exists
            if hasattr(self, 'hand_display') and self.hand_display:
                # Get current hand using the correct method
                hand = self.controller.get_hand()

                # Remove old hand display
                self.remove_widget(self.hand_display)

                # Create new hand display
                self.hand_display = HandDisplay(self.on_card_play)
                self.add_widget(self.hand_display)

                # Display current cards
                if hand:
                    self.hand_display.display_hand(hand, self.builder)

            # ✅ 重新添加 effects_overlay（如果不在了）
            if hasattr(self, 'effects_overlay') and self.effects_overlay:
                # effects_overlay 已经存在，只需要确保它在正确的位置
                if self.effects_overlay in self.children:
                    self.remove_widget(self.effects_overlay)
                self.add_widget(self.effects_overlay)
                print(f"[GameScreen] Re-added effects_overlay at top layer")
            else:
                # effects_overlay 不存在，创建新的
                self.effects_overlay = FloatLayout(
                    size_hint=(1, None),
                    height=0
                )
                self.add_widget(self.effects_overlay)
                print(f"[GameScreen] Created new effects_overlay")

            # ✅ 如果游戏结束了，重新显示游戏结束按钮
            if is_game_over and game_result:
                print(f"[GameScreen] Re-adding game-over buttons for {game_result}")
                
                # ✅ 清理 effects_overlay 中的旧按钮（避免重复添加）
                if hasattr(self, 'effects_overlay') and self.effects_overlay:
                    # 移除所有旧的子元素（按钮、火球等）
                    # old_children = list(self.effects_overlay.children)
                    for child in list(self.effects_overlay.children):
                        if isinstance(child,BoxLayout):
                            self.effects_overlay.remove_widget(child)
                    print(f"[GameScreen] Removed old elements from effects_overlay")
                
                # ✅ 只添加按钮，不重复播放音效和显示文本
                if game_result == 'win':
                    # 不调用 show_win()，避免重复显示文本
                    # 只添加按钮
                    self.button_manager.add_game_over_buttons(
                        restart_text=T.BTN_PLAY_AGAIN['zh'],
                        on_restart=self.on_restart,
                        on_menu=self.on_back_to_menu_clicked
                    )
                else:  # game_result == 'lose'
                    # 不调用 show_lose()，避免重复显示文本
                    # 只添加按钮
                    self.button_manager.add_game_over_buttons(
                        restart_text=T.BTN_TRY_AGAIN['zh'],
                        on_restart=self.on_restart,
                        on_menu=self.on_back_to_menu_clicked
                    )

            print("[GameScreen] UI refresh complete")

        except Exception as e:
            print(f"[GameScreen] Error refreshing UI: {e}")
            import traceback
            traceback.print_exc()
