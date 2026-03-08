"""Main game screen UI - Refactored version."""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from ui.font_config import get_chinese_font_name
from game.game_controller import GameController
from ui.ui_logger import UILogger
from ui.ui_builder import UIBuilder
from ui.hand_display import HandDisplay
from ui.stats_display import StatsDisplay
from ui.animations import Animations
from game.models import CardType
from game.translation_strings import Translations as T


class GameScreen(BoxLayout):
    """Main game screen - simplified to component assembly only."""
    
    def __init__(self, on_back_to_menu):
        """Initialize the game screen."""
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
        """Refresh all displays from controller state."""
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
        
        Args:
            card: Card object to play
        """
        result = self.controller.play_card(card)
        
        if not result['success']:
            print(f"[UI] Play card failed: {result.get('error', 'Unknown error')}")
            return
        
        # Remove card from hand display
        self.hand_display.remove_card(card)
        
        # Update UI
        stats = self.controller.get_stats()
        self.stats_display.update_stats(stats)
        self.stats_display.update_battle_area(
            result['result_text'],
            self.get_card_color(card)
        )
        
        # ✅ ADD: Boss hit animation if damage was dealt
        if card.card_type == CardType.ATTACK or card.card_type == CardType.CRITICAL:
            if self.stats_display.boss_widget:
                self.stats_display.boss_widget.hit_animation()

            # Player attack animation
            if self.stats_display.player_widget:
                self.stats_display.player_widget.attack_animation()

        # Heal animation for heal cards
        elif card.card_type == CardType.HEAL:
            if self.stats_display.player_widget:
                self.stats_display.player_widget.heal_animation()

        self.stats_display.update_cards_played(
            result['cards_played'],
            result['max_cards']
        )
        
        # Check if reached max cards
        if result['cards_played'] >= result['max_cards']:
            self.hand_display.disable_all()
        
        # Check win/lose
        self.check_game_result(result['result'])
    
    def on_end_turn(self, instance):
        """
        Handle end turn button press.
        
        Args:
            instance: Button widget (unused)
        """
        result = self.controller.end_turn()
        
        if not result['success']:
            print(f"[UI] End turn failed: {result.get('error', 'Unknown error')}")
            return
        
        # Update battle area with boss attack result
        self.stats_display.update_battle_area(result['result_text'])
        
        # Check if boss used special attack
        is_special_attack = self.controller.battle.last_attack_was_special
        
        if is_special_attack:
            # Special attack with projectile animation
            print(f"[UI] 🔥 BOSS SPECIAL ATTACK DETECTED - Playing animation...")
            
            # Trigger special attack animation (fireball projectile)
            if self.stats_display.boss_widget and self.stats_display.player_widget:
                boss_anim = self.stats_display.boss_widget.animations
                
                # Define callback to handle post-animation tasks
                def on_special_attack_complete():
                    print(f"[UI] Special attack animation complete")
                    
                    # Hide boss warning after special attack is used
                    self.stats_display.hide_boss_special_attack_warning()

                    # Handle deck depletion warning
                    if result['deck_empty']:
                        self.handle_deck_depletion(result)
                    
                    # Refresh display
                    self.refresh_display()
                    
                    # Re-enable cards
                    self.hand_display.enable_all()
                    
                    # Check win/lose
                    self.check_game_result(result['result'])
                
                # Start special attack animation (pass this GameScreen as parent_widget)
                boss_anim.special_attack_animation(
                    player_widget=self.stats_display.player_widget,
                    parent_widget=self,  # Add projectile to GameScreen
                    callback=on_special_attack_complete
                )
            else:
                print(f"[UI] ERROR: boss_widget or player_widget not found!")
                # Fallback to normal flow
                self._finish_turn(result)
        else:
            # Normal boss attack - use existing animation logic
            if self.stats_display.boss_widget:
                self.stats_display.boss_widget.attack_animation()
            
            # Player hit animation
            if self.stats_display.player_widget:
                self.stats_display.player_widget.hit_animation()
            
            # Finish turn immediately
            self._finish_turn(result)
    
    def _finish_turn(self, result):
        """
        Complete turn processing (for non-special attacks or after animation).
        
        Args:
            result: Result dict from controller
        """
        # Handle deck depletion warning
        if result['deck_empty']:
            self.handle_deck_depletion(result)
        
        # Refresh display
        self.refresh_display()
        
        # Re-enable cards
        self.hand_display.enable_all()
        
        # Check win/lose
        self.check_game_result(result['result'])
    
    def check_game_result(self, result):
        """
        Check and handle game end result.
        
        Args:
            result: 'win', 'lose', or 'playing'
        """
        if result == 'win':
            self.controller.set_game_over(True)
            self.stats_display.show_win(self.controller.battle.turn)
            self.add_restart_button(T.BTN_PLAY_AGAIN['zh'])
        elif result == 'lose':
            self.controller.set_game_over(True)
            self.stats_display.show_lose(self.controller.battle.turn)
            self.add_restart_button(T.BTN_TRY_AGAIN['zh'])
    
    def handle_deck_depletion(self, result):
        """
        Handle deck depletion warnings.
        
        Args:
            result: End turn result dictionary
        """
        stats = self.controller.get_stats()
        
        if stats['cards_in_hand'] == 0:
            msg = "\n" + T.UI_DECK_NO_CARDS['zh']
            self.stats_display.update_battle_area(result['result_text'] + msg, (1, 0.3, 0, 1))
        elif result['cards_drawn'] == 0:
            remaining = stats['cards_in_hand']
            msg = T.UI_DECK_EMPTY_WARNING['zh'].format(remaining)
            self.stats_display.update_battle_area(result['result_text'] + msg, (1, 0.6, 0, 1))
        else:
            msg = T.UI_DECK_LAST_DRAW['zh'].format(result['cards_drawn'])
            self.stats_display.update_battle_area(result['result_text'] + msg, (0.9, 0.7, 0, 1))
    
    def add_restart_button(self, text):
        """
        Add restart and menu buttons to screen.
        
        Args:
            text: Restart button text
        """
        from game.translations import t
        
        # Get Chinese font
        chinese_font = get_chinese_font_name()
        
        # Create a horizontal layout for buttons
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1,
            spacing='10sp'
        )
        
        # Play Again button
        restart_btn = Button(
            text=text,
            font_size='20sp',
            bold=True,
            background_color=(0.2, 0.6, 1, 1),
            font_name=chinese_font  # ✅ ADD THIS LINE
        )
        restart_btn.bind(on_press=self.on_restart)
        button_layout.add_widget(restart_btn)
        
        # Return to Main Menu button
        menu_btn = Button(
            text=T.MENU_BACK_TO_MAIN['zh'],
            font_size='20sp',
            bold=True,
            background_color=(0.8, 0.6, 0.2, 1),  # Orange/yellow
            font_name=chinese_font  # ✅ ADD THIS LINE
        )
        menu_btn.bind(on_press=self.on_back_to_menu_clicked)
        button_layout.add_widget(menu_btn)
        
        self.add_widget(button_layout)
    
    def on_restart(self, instance):
        """
        Handle restart button press.
        
        Args:
            instance: Button widget (unused)
        """
        self.controller.reset()
        
        # Clear and rebuild
        self.clear_widgets()
        self.builder = UIBuilder(self)
        self.stats_display = StatsDisplay()
        self.hand_display = HandDisplay(self.on_card_play)
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
