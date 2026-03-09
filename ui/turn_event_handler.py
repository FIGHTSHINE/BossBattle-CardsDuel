"""Turn event handling and coordination."""

from game.models import CardType


class TurnEventHandler:
    """Handles turn-based events and coordinates responses."""
    
    def __init__(self, controller, game_screen):
        """
        Initialize turn event handler.
        
        Args:
            controller: GameController instance
            game_screen: GameScreen instance (for UI updates)
        """
        self.controller = controller
        self.screen = game_screen
    
    def handle_card_play(self, card):
        """
        Handle card play event.
        
        Args:
            card: Card object to play
        """
        result = self.controller.play_card(card)
        
        if not result['success']:
            print(f"[UI] Play card failed: {result.get('error', 'Unknown error')}")
            return
        
        # ✅ Play card sound effect
        from kivy.app import App #type: ignore Import here to avoid circular import issues
        App.get_running_app().audio_manager.play_sound('card_play')
        
        # Update UI
        self.screen.hand_display.remove_card(card)
        
        stats = self.controller.get_stats()
        self.screen.stats_display.update_stats(stats)
        self.screen.stats_display.update_battle_area(
            result['result_text'],
            self.screen.get_card_color(card)
        )
        
        # Play card animation
        self.screen.animation_manager.play_card_animation(card)
        
        self.screen.stats_display.update_cards_played(
            result['cards_played'],
            result['max_cards']
        )
        
        # Check if reached max cards
        if result['cards_played'] >= result['max_cards']:
            self.screen.hand_display.disable_all()
        
        # Check win/lose
        self.screen.flow_manager.check_game_result(result['result'])
    
    def handle_turn_end(self):
        """
        Handle end turn button press.
        
        Returns:
            bool: True if special attack animation started, False otherwise
        """
        result = self.controller.end_turn()
        
        if not result['success']:
            print(f"[UI] End turn failed: {result.get('error', 'Unknown error')}")
            return False
        
        # Update battle area
        self.screen.stats_display.update_battle_area(result['result_text'])
        
        # Check for special attack
        is_special_attack = self.controller.battle.last_attack_was_special
        
        if is_special_attack:
            return self._handle_special_attack(result)
        else:
            return self._handle_normal_attack(result)
    
    def _handle_normal_attack(self, result):
        """
        Handle normal boss attack.
        
        Args:
            result: End turn result dict
            
        Returns:
            bool: False (no async animation)
        """
        # ✅ Play boss attack sound effect
        from kivy.app import App #type: ignore Import here to avoid circular import issues
        App.get_running_app().audio_manager.play_sound('boss_attack')
        
        # Play attack animations
        self.screen.animation_manager.play_boss_attack_animation(
            is_special=False,
            callback=lambda: self._finish_turn(result)
        )
        return False
    
    def _handle_special_attack(self, result):
        """
        Handle boss special attack with projectile animation.
        
        Args:
            result: End turn result dict
            
        Returns:
            bool: True (async animation started)
        """
        print(f"[UI] BOSS SPECIAL ATTACK DETECTED - Playing animation...")
        
        # ✅ Play boss attack sound effect
        from kivy.app import App #type: ignore Import here to avoid circular import issues
        App.get_running_app().audio_manager.play_sound('boss_attack')
        
        if self.screen.stats_display.boss_widget and self.screen.stats_display.player_widget:
            boss_anim = self.screen.stats_display.boss_widget.animations
            
            # Define callback for animation completion
            def on_special_attack_complete():
                print(f"[UI] Special attack animation complete")
                self.screen.stats_display.hide_boss_special_attack_warning()
                self._finish_turn(result)
            
            # Start special attack animation
            boss_anim.special_attack_animation(
                player_widget=self.screen.stats_display.player_widget,
                parent_widget=self.screen,  # Add projectile to GameScreen
                callback=on_special_attack_complete
            )
            return True
        else:
            print(f"[UI] ERROR: boss_widget or player_widget not found!")
            # Fallback to normal flow
            self._finish_turn(result)
            return False
    
    def _finish_turn(self, result):
        """
        Complete turn processing.
        
        Args:
            result: Result dict from controller
        """
        # Use flow manager to finish turn
        self.screen.flow_manager.finish_turn(result)
        
        # Refresh display
        self.screen.refresh_display()
        
        # Re-enable cards
        self.screen.hand_display.enable_all()