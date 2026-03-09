"""Game battle logic and state management (Refactored)."""

from game.battle.card_effects import CardEffectHandler
from game.battle.turn_manager import TurnManager


class BattleManager:
    """
    Manages the battle state and coordinates between subsystems.
    
    This is a coordinator pattern implementation:
    - CardEffectHandler: Handles all card effect applications
    - TurnManager: Manages turn-based system and boss AI
    - BattleManager: Maintains core state and delegates to specialists
    """
    
    def __init__(self):
        """Initialize battle with default values."""
        print("=" * 50)
        print("[BattleManager] Initializing battle system...")
        
        # Core battle state
        self.boss_max_hp = 300
        self.player_max_hp = 100
        self.boss_hp = self.boss_max_hp
        self.player_hp = self.player_max_hp
        self.boss_damage_min = 6
        self.boss_damage_max = 12
        self.shield = 0
        self.turn = 1
        
        # Turn-based system properties
        self.current_turn = "player"  # "player" or "boss"
        self.cards_played_this_turn = 0
        self.max_draws_per_turn = 2
        self.max_cards_per_turn = 3
        
        # Boss special attack system
        self.boss_special_attack_used = False
        self.boss_special_attack_threshold = 0.4  # 40% HP threshold
        self.boss_special_attack_damage = 90
        self.last_attack_was_special = False
        
        # Initialize subsystem managers
        self.turn_manager = TurnManager(self)
        
        print(f"[BattleManager] Battle initialized!")
        print(f"  - Boss HP: {self.boss_hp}/{self.boss_max_hp}")
        print(f"  - Player HP: {self.player_hp}/{self.player_max_hp}")
        print(f"  - Max Cards per Turn: {self.max_cards_per_turn}")
        print(f"  - Boss Damage: {self.boss_damage_min}-{self.boss_damage_max}")
        print("=" * 50)
    
    def play_card(self, card):
        """
        Play a card and apply its effects.
        
        Delegates to CardEffectHandler for all card-specific logic.
        
        Args:
            card: Card object to play
            
        Returns:
            tuple: (result, result_text) where result is 'win', 'lose', or 'playing'
        """
        print(f"\n[PLAY_CARD] Playing card: {card.name} "
              f"(Type: {card.card_type.value}, Value: {card.value})")
        
        try:
            # Delegate card effect to CardEffectHandler
            result_text, _ = CardEffectHandler.apply_card(self, card)
            
            # Increment cards played this turn
            self.cards_played_this_turn += 1
            print(f"[TURN] Cards played this turn: "
                  f"{self.cards_played_this_turn}/{self.max_cards_per_turn}")
            
            # Check win condition (boss defeated)
            if self.boss_hp <= 0:
                print(f"\n[WIN] Boss defeated! Final HP: {max(0, self.boss_hp)}")
                return "win", result_text
            
            # Game continues
            print(f"[STATE] Boss: {self.boss_hp}/{self.boss_max_hp} | "
                  f"Player: {self.player_hp}/{self.player_max_hp} | Shield: {self.shield}")
            return "playing", result_text
            
        except Exception as e:
            print(f"[ERROR] Exception in play_card: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return "playing", f"Error playing card: {e}"
    
    def end_player_turn(self):
        """
        End player turn and execute boss attack.
        
        Delegates to TurnManager for turn logic and boss AI.
        
        Returns:
            tuple: (result, result_text) where result is 'win', 'lose', or 'playing'
        """
        return self.turn_manager.end_player_turn()
    
    def is_player_turn(self):
        """
        Check if it's currently the player's turn.
        
        Delegates to TurnManager.
        
        Returns:
            bool: True if player's turn, False if boss's turn
        """
        return self.turn_manager.is_player_turn()
    
    def can_play_card(self):
        """
        Check if player can play a card.
        
        Delegates to TurnManager.
        
        Returns:
            bool: True if card can be played, False otherwise
        """
        return self.turn_manager.can_play_card()
    
    def reset(self):
        """Reset battle to initial state."""
        print(f"\n{'=' * 50}")
        print("[RESET] Resetting battle state...")
        
        # Reset core state
        self.boss_hp = self.boss_max_hp
        self.player_hp = self.player_max_hp
        self.shield = 0
        self.turn = 1
        
        # Reset turn-based system
        self.current_turn = "player"
        self.cards_played_this_turn = 0
        
        # Reset boss special attack flags
        self.boss_special_attack_used = False
        self.last_attack_was_special = False
        print(f"[RESET] Boss special attack reset: can_use=True")
        
        print(f"[RESET] Battle reset complete!")
        print(f"  - Boss HP: {self.boss_hp}/{self.boss_max_hp}")
        print(f"  - Player HP: {self.player_hp}/{self.player_max_hp}")
        print(f"  - Turn: {self.turn}")
        print(f"=" * 50)