"""UI handler for updating and managing UI components."""

from ui.animations import Animations
from ui.ui_logger import UILogger
from game.models import CardType
from game.translations import t, language_manager
from utils.screen_config import ScreenConfig

class UIHandler:
    """Handles UI updates and events."""
    
    def __init__(self, parent_layout):
        """
        Initialize UI handler.
        
        Args:
            parent_layout: The parent GameScreen instance
        """
        self.parent = parent_layout
        self.logger = UILogger()
        self.lang = language_manager.current_language
    
    def update_ui(self, battle, result_text, card, cards_remaining):
        """
        Update all UI elements after game state change.
        
        Args:
            battle: BattleManager instance
            result_text: Text to display in battle area
            card: Card that was played (can be None)
            cards_remaining: Number of cards remaining
        """
        self.logger.log_ui_update_start()
        
        try:
            # Update HP and shield labels
            self.parent.boss_label.text = t('UI_BOSS_HP', max(0, battle.boss_hp), battle.boss_max_hp)
            self.parent.player_label.text = t('UI_PLAYER_HP', max(0, battle.player_hp), battle.player_max_hp)
            self.parent.shield_label.text = t('UI_SHIELD', battle.shield)
            self.parent.cards_label.text = t('UI_CARDS_REMAINING', cards_remaining)
            self.parent.turn_label.text = t('UI_TURN_COUNTER', battle.turn)
            
            # Update battle area
            self.parent.battle_area.text = result_text
            
            # Color feedback based on card type
            if card is not None:
                if card.card_type == CardType.HEAL:
                    self.parent.battle_area.color = (0.2, 1, 0.5, 1)
                elif card.card_type == CardType.SHIELD:
                    self.parent.battle_area.color = (0.3, 0.7, 1, 1)
                elif card.card_type == CardType.CRITICAL:
                    self.parent.battle_area.color = (0.9, 0.3, 1, 1)
                else:
                    self.parent.battle_area.color = (0.9, 0.9, 0.9, 1)
                
                # Animate damage
                if card.card_type in [CardType.ATTACK, CardType.CRITICAL]:
                    self.logger.log_damage_animation()
                    Animations.damage_flash(self.parent.boss_label)
            
            # Update turn indicator
            self.update_turn_indicator(battle)
            
            # Low HP warning
            if battle.player_hp <= 30:
                self.parent.player_label.color = (1, 0.3, 0.3, 1)
                self.logger.log_low_hp_warning(battle.player_hp)
            else:
                self.parent.player_label.color = (0.3, 1, 0.3, 1)
            
            self.logger.log_ui_update_success()
            
        except Exception as e:
            self.logger.log_error("update_ui", e)
    
    def update_turn_indicator(self, battle):
        """
        Update turn indicator display.
        
        Args:
            battle: BattleManager instance
        """
        try:
            if battle.is_player_turn():
                self.parent.turn_indicator.text = t('UI_TURN_PLAYER')
                self.parent.turn_indicator.color = (0.3, 1, 0.5, 1)  # Green
                self.logger.log_turn_indicator_player()
            else:
                self.parent.turn_indicator.text = t('UI_TURN_BOSS')
                self.parent.turn_indicator.color = (1, 0.3, 0.3, 1)  # Red
                self.logger.log_turn_indicator_boss()
        except Exception as e:
            self.logger.log_error_no_traceback("update_turn_indicator", e)
    
    def disable_all_cards(self):
        """Disable all card buttons."""
        self.logger.log_disabling_cards()
        try:
            count = 0
            for widget in self.parent.card_widgets.values():
                widget.disabled = True
                count += 1
            self.logger.log_cards_disabled(count)
        except Exception as e:
            self.logger.log_error("disable_all_cards", e)
    
    def enable_all_cards(self):
        """Enable all card buttons."""
        self.logger.log_enabling_cards()
        try:
            count = 0
            for widget in self.parent.card_widgets.values():
                widget.disabled = False
                count += 1
            self.logger.log_cards_enabled(count)
        except Exception as e:
            self.logger.log_error("enable_all_cards", e)
    
    def remove_card_widget(self, card):
        """
        Remove a card widget from the UI.
        
        Args:
            card: Card object to remove
        """
        self.logger.log_removing_card(card.name)
        
        try:
            # Check if unique_id exists in card_widgets
            if card.unique_id in self.parent.card_widgets:
                widget = self.parent.card_widgets[card.unique_id]
                
                # Remove from layout if it exists
                if widget in self.parent.card_layout.children:
                    self.parent.card_layout.remove_widget(widget)
                
                # Remove from dictionary
                del self.parent.card_widgets[card.unique_id]
                self.logger.log_card_removed()
                
            else:
                # Card not found in dictionary
                self.logger.log_card_not_found()
                print(f"[WARNING] Card ID {card.unique_id} not found in card_widgets")
                print(f"[DEBUG] Available IDs: {list(self.parent.card_widgets.keys())}")
                print(f"[DEBUG] Card name: {card.name}, type: {card.card_type.value}")
                
        except Exception as e:
            self.logger.log_error("remove_card_widget", e)
    
    def show_win(self, turns):
        """
        Show victory screen.
        
        Args:
            turns: Number of turns taken
        """
        self.logger.log_win(turns)
        
        try:
            self.parent.boss_label.color = (0, 1, 0, 1)
            victory_text = t('MSG_VICTORY', turns)
            self.parent.battle_area.text = f"{ScreenConfig.get_markup_size(28)}[color=00ff00]{victory_text}[/color][/size]"
            self.parent.battle_area.color = (0, 1, 0, 1)
            self.logger.log_win_screen_displayed()
        except Exception as e:
            self.logger.log_error("show_win", e)
    
    def show_lose(self, turns):
        """
        Show defeat screen.
        
        Args:
            turns: Number of turns survived
        """
        self.logger.log_lose(turns)
        
        try:
            self.parent.player_label.color = (1, 0, 0, 1)
            defeat_text = t('MSG_DEFEAT', turns)
            self.parent.battle_area.text = f"{ScreenConfig.get_markup_size(28)}[color=ff3333]{defeat_text}[/color][/size]"
            self.parent.battle_area.color = (1, 0.2, 0.2, 1)
            self.logger.log_lose_screen_displayed()
        except Exception as e:
            self.logger.log_error("show_lose", e)
    
    def add_restart_button(self, result_type, callback):
        """
        Add restart button to the screen.
        
        Args:
            result_type: 'win' or 'lose'
            callback: Function to call when button is pressed
        """
        if result_type == "win":
            button_text = t('BTN_PLAY_AGAIN')
        else:
            button_text = t('BTN_TRY_AGAIN')
        
        self.logger.log_restart_button_added(button_text)
        try:
            from ui.ui_builder import UIBuilder
            builder = UIBuilder(self.parent)
            restart_btn = builder.build_restart_button(button_text, callback)
            self.parent.add_widget(restart_btn)
            self.logger.log_restart_button_added_success()
        except Exception as e:
            self.logger.log_error("add_restart_button", e)
    
    def update_cards_played_counter(self, cards_played, max_cards):
        """
        Update cards played counter label.
        
        Args:
            cards_played: Number of cards played this turn
            max_cards: Maximum cards allowed per turn
        """
        self.parent.cards_played_label.text = t('UI_CARDS_THIS_TURN', cards_played, max_cards)
        self.logger.log_counter_update(cards_played, max_cards)