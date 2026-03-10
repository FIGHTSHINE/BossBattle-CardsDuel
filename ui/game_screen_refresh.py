"""UI refresh manager for GameScreen - handles complex refresh logic."""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from ui.hand_display import HandDisplay
from ui.stats_display import StatsDisplay
from ui.game_managers import GameAnimationManager, GameFlowManager, GameButtonManager
from game.translations import Translations as T
from utils.screen_config import ScreenConfig


class GameScreenRefreshManager:
    """
    Manages UI refresh logic for GameScreen.
    
    This class encapsulates the complex logic of refreshing UI elements
    when screen size changes, including:
    - Preserving game state during refresh
    - Rebuilding UI components with new scaling
    - Restoring effects overlay and game-over buttons
    """
    
    def __init__(self, game_screen):
        """
        Initialize the refresh manager.
        
        Args:
            game_screen: The GameScreen instance to manage
        """
        self.screen = game_screen
        print("[GameScreenRefreshManager] Initialized")
    
    def refresh_ui(self):
        """
        Refresh all UI elements with current screen scaling.

        Preserves game state and re-adds game-over buttons if needed.
        This method is called when window is resized.
        """
        try:
            print("[GameScreenRefreshManager] Refreshing UI scaling...")

            # Check if game is over and preserve result
            is_game_over = self.screen.controller.is_game_over()
            game_result = self._get_game_result(is_game_over)
            
            # Preserve effects overlay children
            overlay_children = self._preserve_overlay_children()

            # Refresh layout properties
            self._refresh_layout_properties()

            # Rebuild stats display
            self._rebuild_stats_display()

            # Rebuild hand display
            self._rebuild_hand_display()

            # Ensure effects overlay is at top layer
            self._ensure_effects_overlay()

            # Restore game-over buttons if needed
            self._restore_game_over_buttons(is_game_over, game_result, overlay_children)

            print("[GameScreenRefreshManager] UI refresh complete")

        except Exception as e:
            print(f"[GameScreenRefreshManager ERROR] Refresh failed: {str(e)}")
            import traceback
            print(f"[GameScreenRefreshManager ERROR] Traceback:\n{traceback.format_exc()}")
    
    def _get_game_result(self, is_game_over):
        """
        Determine game result (win/lose) if game is over.
        
        Args:
            is_game_over: Whether the game has ended
            
        Returns:
            str: 'win', 'lose', or None
        """
        if not is_game_over:
            return None
        
        stats = self.screen.controller.get_stats()
        if stats['boss_hp'] <= 0:
            result = 'win'
        elif stats['player_hp'] <= 0:
            result = 'lose'
        else:
            result = None
        
        print(f"[GameScreenRefreshManager] Game result: {result}")
        return result
    
    def _preserve_overlay_children(self):
        """
        Preserve current effects overlay children before refresh.
        
        Returns:
            list: Current children of effects_overlay
        """
        overlay_children = []
        if hasattr(self.screen, 'effects_overlay') and self.screen.effects_overlay:
            overlay_children = list(self.screen.effects_overlay.children)
            print(f"[GameScreenRefreshManager] Preserved {len(overlay_children)} overlay children")
        return overlay_children
    
    def _refresh_layout_properties(self):
        """Refresh padding and spacing based on current screen size."""
        self.screen.padding = ScreenConfig.scale_padding(20)
        self.screen.spacing = ScreenConfig.scale_spacing(10)
        print("[GameScreenRefreshManager] Layout properties refreshed")
    
    def _rebuild_stats_display(self):
        """Rebuild stats display with current scaling."""
        if not (hasattr(self.screen, 'stats_display') and self.screen.stats_display):
            return
        
        # Get current stats before rebuilding
        stats = self.screen.controller.get_stats()

        # Remove old stats display
        self.screen.remove_widget(self.screen.stats_display)

        # Create new stats display
        self.screen.stats_display = StatsDisplay()
        self.screen.stats_display.build_stats(self.screen.builder)
        self.screen.add_widget(self.screen.stats_display, index=0)  # Add at top

        # Update stats with current values
        self.screen.stats_display.update_stats(stats)
        self.screen.stats_display.update_turn_indicator(stats['is_player_turn'])
        self.screen.stats_display.update_cards_played(
            self.screen.controller.battle.cards_played_this_turn,
            self.screen.controller.battle.max_cards_per_turn
        )

        # Re-add end turn button
        self.screen.stats_display.add_end_turn_button(self.screen.on_end_turn)
        
        print("[GameScreenRefreshManager] Stats display rebuilt")
    
    def _rebuild_hand_display(self):
        """Rebuild hand display with current scaling."""
        if not (hasattr(self.screen, 'hand_display') and self.screen.hand_display):
            return
        
        # Get current hand
        hand = self.screen.controller.get_hand()

        # Remove old hand display
        self.screen.remove_widget(self.screen.hand_display)

        # Create new hand display
        self.screen.hand_display = HandDisplay(self.screen.on_card_play)
        self.screen.add_widget(self.screen.hand_display)

        # Display current cards
        if hand:
            self.screen.hand_display.display_hand(hand, self.screen.builder)
        
        print("[GameScreenRefreshManager] Hand display rebuilt")
    
    def _ensure_effects_overlay(self):
        """Ensure effects_overlay exists and is at the top layer."""
        if hasattr(self.screen, 'effects_overlay') and self.screen.effects_overlay:
            # effects_overlay exists, ensure it's at top
            if self.screen.effects_overlay in self.screen.children:
                self.screen.remove_widget(self.screen.effects_overlay)
            self.screen.add_widget(self.screen.effects_overlay)
            print("[GameScreenRefreshManager] Effects overlay re-added at top layer")
        else:
            # Create new effects_overlay
            self.screen.effects_overlay = FloatLayout(
                size_hint=(1, None),
                height=0
            )
            self.screen.add_widget(self.screen.effects_overlay)
            print("[GameScreenRefreshManager] Created new effects overlay")
    
    def _restore_game_over_buttons(self, is_game_over, game_result, overlay_children):
        """
        Restore game-over buttons if game was over.
        
        Args:
            is_game_over: Whether the game has ended
            game_result: 'win' or 'lose' or None
            overlay_children: Previously preserved overlay children
        """
        if not (is_game_over and game_result):
            return
        
        print(f"[GameScreenRefreshManager] Restoring game-over buttons for {game_result}")
        
        # Clear old elements from effects_overlay to avoid duplicates
        if hasattr(self.screen, 'effects_overlay') and self.screen.effects_overlay:
            for child in list(self.screen.effects_overlay.children):
                if isinstance(child, BoxLayout):
                    self.screen.effects_overlay.remove_widget(child)
            print("[GameScreenRefreshManager] Removed old elements from effects_overlay")
        
        # Add game-over buttons (without replaying sounds or showing text)
        if game_result == 'win':
            self.screen.button_manager.add_game_over_buttons(
                restart_text=T.BTN_PLAY_AGAIN['zh'],
                on_restart=self.screen.on_restart,
                on_menu=self.screen.on_back_to_menu_clicked
            )
        else:  # game_result == 'lose'
            self.screen.button_manager.add_game_over_buttons(
                restart_text=T.BTN_TRY_AGAIN['zh'],
                on_restart=self.screen.on_restart,
                on_menu=self.screen.on_back_to_menu_clicked
            )
        
        print("[GameScreenRefreshManager] Game-over buttons restored")