"""Game flow and state transition manager."""

from kivy.app import App
from game.translations import Translations as T


class GameFlowManager:
    """Manages game flow transitions and end-game scenarios."""
    
    def __init__(self, controller, stats_display, animation_manager, button_manager=None, game_screen=None):
        """
        Initialize game flow manager.
        
        Args:
            controller: GameController instance
            stats_display: StatsDisplay instance
            animation_manager: GameAnimationManager instance
            button_manager: GameButtonManager instance (optional, for adding game-over buttons)
            game_screen: GameScreen instance (optional, for button callbacks)
        """
        self.controller = controller
        self.stats_display = stats_display
        self.animation_manager = animation_manager
        self.button_manager = button_manager
        self.game_screen = game_screen
    
    def check_game_result(self, result):
        """
        Check and handle game end result.
        
        Args:
            result: 'win', 'lose', or 'playing'
        """
        if result == 'win':
            self._handle_victory()
        elif result == 'lose':
            self._handle_defeat()
    
    def _handle_victory(self):
        """Handle victory scenario."""
        self.controller.set_game_over(True)
        
        # ✅ Stop battle music before playing victory sound
        App.get_running_app().audio_manager.stop_all_music()
        
        # Play victory sound
        App.get_running_app().audio_manager.play_sound('victory')
        
        # Show victory screen
        self.stats_display.show_win(self.controller.battle.turn)
        
        # Add game-over buttons
        self._add_game_over_buttons(T.BTN_PLAY_AGAIN['zh'])
    
    def _handle_defeat(self):
        """Handle defeat scenario."""
        self.controller.set_game_over(True)
        
        # ✅ Stop battle music before playing defeat sound
        App.get_running_app().audio_manager.stop_all_music()
        
        # Play defeat sound
        App.get_running_app().audio_manager.play_sound('defeat')
        
        # Show defeat screen
        self.stats_display.show_lose(self.controller.battle.turn)
        
        # Add game-over buttons
        self._add_game_over_buttons(T.BTN_TRY_AGAIN['zh'])
    
    def _add_game_over_buttons(self, restart_text):
        """
        Add restart and menu buttons when game ends.
        
        Args:
            restart_text: Text for restart button
        """
        if self.button_manager and self.game_screen:
            self.button_manager.add_game_over_buttons(
                restart_text=restart_text,
                on_restart=self.game_screen.on_restart,
                on_menu=self.game_screen.on_back_to_menu_clicked
            )
        else:
            print("[WARNING] button_manager or game_screen not set - cannot add game-over buttons")
    
    def handle_deck_depletion(self, result):
        """
        Handle deck depletion warnings.
        
        Args:
            result: End turn result dictionary
        """
        stats = self.controller.get_stats()
        
        if stats['cards_in_hand'] == 0:
            msg = "\n" + T.UI_DECK_NO_CARDS['zh']
            self.stats_display.update_battle_area(
                result['result_text'] + msg, 
                (1, 0.3, 0, 1)
            )
        elif result['cards_drawn'] == 0:
            remaining = stats['cards_in_hand']
            msg = T.UI_DECK_EMPTY_WARNING['zh'].format(remaining)
            self.stats_display.update_battle_area(
                result['result_text'] + msg, 
                (1, 0.6, 0, 1)
            )
        else:
            msg = T.UI_DECK_LAST_DRAW['zh'].format(result['cards_drawn'])
            self.stats_display.update_battle_area(
                result['result_text'] + msg, 
                (0.9, 0.7, 0, 1)
            )
    
    def finish_turn(self, result):
        """
        Complete turn processing.
        
        Args:
            result: Result dict from controller
        """
        # Handle deck depletion warning
        if result['deck_empty']:
            self.handle_deck_depletion(result)
        
        # Check game result
        self.check_game_result(result['result'])