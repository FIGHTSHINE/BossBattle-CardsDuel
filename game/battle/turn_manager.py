"""Turn management system for battle."""

from game.battle.boss_ai import BossAI
from game.translations import Translations as T


class TurnManager:
    """Manages turn-based battle system."""
    
    def __init__(self, battle_manager):
        """
        Initialize turn manager.
        
        Args:
            battle_manager: Reference to BattleManager instance
        """
        self.battle = battle_manager
        self.boss_ai = BossAI(battle_manager)
    
    def end_player_turn(self):
        """
        End player turn and execute boss attack.
        
        Returns:
            tuple: (result, result_text) where result is 'win', 'lose', or 'playing'
        """
        print(f"\n{'=' * 50}")
        print(f"[TURN] Ending player turn (Cards played: {self.battle.cards_played_this_turn})")
        
        # Switch to boss turn
        self.battle.current_turn = "boss"
        print(f"[TURN] Switched to BOSS TURN")
        
        # Let Boss AI decide action
        try:
            action_type, _ = self.boss_ai.decide_action()
            
            if action_type == 'special':
                result, result_text = self.boss_ai.execute_special_attack()
            else:
                result, result_text = self.boss_ai.execute_normal_attack()
            
            # If battle continues, switch back to player turn
            if result == 'playing':
                self.battle.current_turn = "player"
                self.battle.cards_played_this_turn = 0
                self.battle.turn += 1
                
                print(f"[TURN] Switched to PLAYER TURN (Turn {self.battle.turn})")
                print(f"=" * 50)
            
            return result, result_text
            
        except Exception as e:
            print(f"[ERROR] Exception in end_player_turn: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return "playing", T.MSG_ERROR_END_TURN['zh'].format(e)
    
    def is_player_turn(self):
        """
        Check if it's currently the player's turn.
        
        Returns:
            bool: True if player's turn, False if boss's turn
        """
        result = self.battle.current_turn == "player"
        print(f"[DEBUG] is_player_turn: {result} (current: {self.battle.current_turn})")
        return result
    
    def can_play_card(self):
        """
        Check if player can play a card.
        
        Returns:
            bool: True if card can be played, False otherwise
        """
        is_player = self.is_player_turn()
        under_limit = self.battle.cards_played_this_turn < self.battle.max_cards_per_turn
        can_play = is_player and under_limit
        
        if not can_play:
            if not is_player:
                print(f"[BLOCK] Cannot play card: Not player's turn (current: {self.battle.current_turn})")
            elif not under_limit:
                print(f"[BLOCK] Cannot play card: Max cards reached "
                      f"({self.battle.cards_played_this_turn}/{self.battle.max_cards_per_turn})")
        
        return can_play