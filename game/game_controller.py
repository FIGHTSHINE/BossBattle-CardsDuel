"""Game controller - manages game logic and flow."""

from game.battle_manager import BattleManager
from game.card_manager import CardManager
from game.translations import Translations as T


class GameController:
    """Controls the game logic and coordinates components."""
    
    def __init__(self):
        """Initialize game controller."""
        self.battle = BattleManager()
        self.card_manager = CardManager(max_hand_size=5)
        self.game_over = False
        self.turn = 1
        
        print("[GameController] Game initialized")
    
    def play_card(self, card):
        """
        Play a card.
        
        Args:
            card: Card object to play
            
        Returns:
            dict: Result with keys: 'success', 'result', 'result_text', 'error'
        """
        if self.game_over:
            return {'success': False, 'error': T.MSG_ERROR_GAME_OVER['zh']}
        
        if not self.battle.can_play_card():
            return {'success': False, 'error': T.MSG_ERROR_CANNOT_PLAY['zh']}
        
        try:
            # Remove card from hand using CardManager
            if not self.card_manager.play_card(card):
                return {'success': False, 'error': 'Card not in hand'}
            
            # Apply card effects
            result, result_text = self.battle.play_card(card)
            
            return {
                'success': True,
                'result': result,
                'result_text': result_text,
                'cards_played': self.battle.cards_played_this_turn,
                'max_cards': self.battle.max_cards_per_turn
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def end_turn(self):
        """
        End player turn and execute boss turn.
        
        Returns:
            dict: Result with keys: 'success', 'result', 'result_text', 
                   'cards_drawn', 'deck_empty', 'error'
        """
        if self.game_over:
            return {'success': False, 'error': 'Game is over'}
        
        if not self.battle.is_player_turn():
            return {'success': False, 'error': T.MSG_ERROR_NOT_TURN['zh']}
        
        try:
            # Execute boss turn
            result, result_text = self.battle.end_player_turn()
            
            # Draw cards limit for next turn
            cards_drawn, deck_empty = self.card_manager.refill_hand(max_draws=self.battle.max_draws_per_turn)
            
            return {
                'success': True,
                'result': result,
                'result_text': result_text,
                'cards_drawn': cards_drawn,
                'deck_empty': deck_empty,
                'turn': self.battle.turn
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_hand(self):
        """Get current hand."""
        return self.card_manager.get_hand()
    
    def get_stats(self):
        """Get current game stats."""
        return {
            'boss_hp': self.battle.boss_hp,
            'boss_max_hp': self.battle.boss_max_hp,
            'player_hp': self.battle.player_hp,
            'player_max_hp': self.battle.player_max_hp,
            'shield': self.battle.shield,
            'turn': self.battle.turn,
            'is_player_turn': self.battle.is_player_turn(),
            'cards_in_hand': len(self.card_manager.hand),
            'cards_in_deck': len(self.card_manager.draw_pile),
            'cards_used': len(self.card_manager.discard_pile),
            'cards_total_remaining': self.card_manager.cards_total_remaining()
        }
    
    def is_game_over(self):
        """Check if game is over."""
        return self.game_over
    
    def set_game_over(self, value):
        """Set game over state."""
        self.game_over = value
    
    def reset(self):
        """Reset the game."""
        self.battle.reset()
        self.card_manager = CardManager(max_hand_size=5)
        self.game_over = False
        print("[GameController] Game reset")