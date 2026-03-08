"""Game battle logic and state management."""

import random
from game.translation_strings import Translations as T

class BattleManager:
    """Manages the battle state and rules."""
    
    def __init__(self):
        """Initialize battle with default values."""
        print("=" * 50)
        print("[BattleManager] Initializing battle system...")
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
        self.max_draws_per_turn = 2  # turn draw limit 2
        self.max_cards_per_turn = 3
        # Boss special attack system
        self.boss_special_attack_used = False
        self.boss_special_attack_threshold = 0.4  # 40% HP threshold
        self.boss_special_attack_damage = 90
        self.last_attack_was_special = False

        print(f"[BattleManager] Battle initialized!")
        print(f"  - Boss HP: {self.boss_hp}/{self.boss_max_hp}")
        print(f"  - Player HP: {self.player_hp}/{self.player_max_hp}")
        print(f"  - Max Cards per Turn: {self.max_cards_per_turn}")
        print(f"  - Boss Damage: {self.boss_damage_min}-{self.boss_damage_max}")
        print("=" * 50)
    
    def play_card(self, card):
        """
        Play a card and apply its effects.
        
        Args:
            card: Card object to play
            
        Returns:
            tuple: (result, result_text) where result is 'win', 'lose', or 'playing'
        """
        print(f"\n[PLAY_CARD] Playing card: {card.name} (Type: {card.card_type.value}, Value: {card.value})")
        
        result_text = ""
        
        try:
            # Apply card effect
            if card.card_type.value == "attack":
                self.boss_hp -= card.value
                result_text = f"⚔️ Used {card.name}! Dealt {card.value} damage!"
                print(f"[EFFECT] Attack: Boss HP {self.boss_hp + card.value} → {self.boss_hp}")
                
            elif card.card_type.value == "critical":
                # Critical hits have 20% chance to do double damage
                if random.random() < 0.2:
                    damage = card.value * 2
                    self.boss_hp -= damage
                    result_text = f"💥 CRITICAL HIT! {card.name} deals {damage} damage!"
                    print(f"[EFFECT] CRITICAL HIT! Boss HP {self.boss_hp + damage} → {self.boss_hp}")
                else:
                    self.boss_hp -= card.value
                    result_text = f"⚔️ Used {card.name}! Dealt {card.value} damage!"
                    print(f"[EFFECT] Attack: Boss HP {self.boss_hp + card.value} → {self.boss_hp}")
                    
            elif card.card_type.value == "heal":
                heal_amount = min(card.value, self.player_max_hp - self.player_hp)
                self.player_hp += heal_amount
                result_text = f"💚 Healed {heal_amount} HP!"
                print(f"[EFFECT] Heal: Player HP {self.player_hp - heal_amount} → {self.player_hp}")
                
            elif card.card_type.value == "shield":
                self.shield = card.value
                result_text = T.MSG_SHIELD_UP['zh'].format(card.value)
                print(f"[EFFECT] Shield: Shield value set to {self.shield}")
            
            # Increment cards played this turn
            self.cards_played_this_turn += 1
            print(f"[TURN] Cards played this turn: {self.cards_played_this_turn}/{self.max_cards_per_turn}")
            
            # Check win condition (boss defeated)
            if self.boss_hp <= 0:
                print(f"\n[WIN] Boss defeated! Final HP: {max(0, self.boss_hp)}")
                return "win", result_text
            
            # Game continues
            print(f"[STATE] Boss: {self.boss_hp}/{self.boss_max_hp} | Player: {self.player_hp}/{self.player_max_hp} | Shield: {self.shield}")
            return "playing", result_text
            
        except Exception as e:
            print(f"[ERROR] Exception in play_card: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return "playing", f"Error playing card: {e}"
    
    def end_player_turn(self):
        """
        End player turn and execute boss attack.
        
        Returns:
            tuple: (result, result_text) where result is 'win', 'lose', or 'playing'
        """
        print(f"\n{'=' * 50}")
        print(f"[TURN] Ending player turn (Cards played: {self.cards_played_this_turn})")
        
        # Switch to boss turn
        self.current_turn = "boss"
        print(f"[TURN] Switched to BOSS TURN")
        
        # Check if boss should use special attack
        boss_hp_percent = self.boss_hp / self.boss_max_hp
        if (not self.boss_special_attack_used and 
            boss_hp_percent <= self.boss_special_attack_threshold):
            print(f"[SPECIAL ATTACK] Boss triggers special attack!")
            print(f"[SPECIAL ATTACK] Boss HP: {boss_hp_percent*100:.1f}% <= {self.boss_special_attack_threshold*100:.1f}%")
            return self._execute_boss_special_attack()
        
        # Regular boss attack
        damage = random.randint(self.boss_damage_min, self.boss_damage_max)
        result_text = ""
        self.last_attack_was_special = False  # Reset flag for normal attack
        
        try:
            # Calculate shield reduction
            if self.shield > 0:
                blocked = min(self.shield, damage)
                actual_damage = damage - blocked
                self.shield -= blocked
                # ✅ 修复：根据是否受到伤害选择不同的消息
                if actual_damage > 0:
                    self.player_hp -= actual_damage
                    result_text = T.MSG_BOSS_ATTACK_BLOCKED_PARTIAL['zh'].format(blocked, actual_damage)
                else:
                    # 护盾完全格挡，没有受到伤害
                    result_text = T.MSG_BOSS_ATTACK_BLOCKED['zh'].format(blocked)
                print(f"[BOSS ATTACK] Damage: {damage} | Blocked: {blocked} | Actual Damage: {actual_damage}")
            else:
                self.player_hp -= damage
                result_text = T.MSG_BOSS_ATTACK_NO_SHIELD['zh'].format(damage)
                print(f"[BOSS ATTACK] Damage: {damage} | No shield")
            
            print(f"[STATE] Boss: {self.boss_hp}/{self.boss_max_hp} | Player: {self.player_hp}/{self.player_max_hp} | Shield: {self.shield}")
            
            # Check win/lose conditions
            if self.boss_hp <= 0:
                print(f"\n[WIN] Boss defeated!")
                return "win", result_text
            elif self.player_hp <= 0:
                print(f"\n[LOSE] Player defeated! Final HP: {max(0, self.player_hp)}")
                return "lose", result_text
            
            # Switch back to player turn
            self.current_turn = "player"
            self.cards_played_this_turn = 0
            self.turn += 1
            
            print(f"[TURN] Switched to PLAYER TURN (Turn {self.turn})")
            print(f"=" * 50)
            
            return "playing", result_text
            
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
        result = self.current_turn == "player"
        print(f"[DEBUG] is_player_turn: {result} (current: {self.current_turn})")
        return result
    
    def can_play_card(self):
        """
        Check if player can play a card.
        
        Returns:
            bool: True if card can be played, False otherwise
        """
        is_player = self.is_player_turn()
        under_limit = self.cards_played_this_turn < self.max_cards_per_turn
        can_play = is_player and under_limit
        
        if not can_play:
            if not is_player:
                print(f"[BLOCK] Cannot play card: Not player's turn (current: {self.current_turn})")
            elif not under_limit:
                print(f"[BLOCK] Cannot play card: Max cards reached ({self.cards_played_this_turn}/{self.max_cards_per_turn})")
        
        return can_play
    
    def reset(self):
        """Reset battle to initial state."""
        print(f"\n{'=' * 50}")
        print("[RESET] Resetting battle state...")
        self.boss_hp = self.boss_max_hp
        self.player_hp = self.player_max_hp
        self.shield = 0
        self.turn = 1
        
        # Reset turn-based system
        self.current_turn = "player"
        self.cards_played_this_turn = 0

        # ⚠️ ADD: Reset boss special attack flags
        self.boss_special_attack_used = False
        self.last_attack_was_special = False
        print(f"[RESET] Boss special attack reset: can_use=True")
        
        print(f"[RESET] Battle reset complete!")
        print(f"  - Boss HP: {self.boss_hp}/{self.boss_max_hp}")
        print(f"  - Player HP: {self.player_hp}/{self.player_max_hp}")
        print(f"  - Turn: {self.turn}")
        print(f"=" * 50)

    
    
    def _execute_boss_special_attack(self):
        """
        Execute boss special attack (90 damage, one-time use).
        
        Called when boss HP drops below 40% and special attack hasn't been used yet.
        
        Returns:
            tuple: (result, result_text) where result is 'win', 'lose', or 'playing'
        """
        print(f"\n{'=' * 50}")
        print(f"[SPECIAL ATTACK] ⚠️ BOSS ENRAGED - SPECIAL ATTACK! ⚠️")
        
        damage = self.boss_special_attack_damage
        result_text = ""
        
        # Mark special attack as used
        self.boss_special_attack_used = True
        self.last_attack_was_special = True
        print(f"[SPECIAL ATTACK] Special attack activated ({damage} damage)")
        print(f"[SPECIAL ATTACK] Boss HP: {self.boss_hp}/{self.boss_max_hp} ({self.boss_hp/self.boss_max_hp*100:.1f}%)")
        
        try:
            # Apply damage with shield absorption (same logic as normal attack)
            if self.shield > 0:
                blocked = min(self.shield, damage)
                actual_damage = damage - blocked
                self.shield -= blocked
                # ✅ fix: Use different messages based on whether damage was taken or fully blocked
                if actual_damage > 0:
                    self.player_hp -= actual_damage
                    result_text = T.MSG_BOSS_SPECIAL_BLOCKED_PARTIAL['zh'].format(blocked, actual_damage)
                else:
                    # shield fully blocked the special attack, no damage taken
                    result_text = T.MSG_BOSS_SPECIAL_BLOCKED['zh'].format(blocked)
                print(f"[SPECIAL ATTACK] Damage: {damage} | Blocked: {blocked} | Actual Damage: {actual_damage}")
            else:
                self.player_hp -= damage
                result_text = T.MSG_BOSS_SPECIAL_NO_SHIELD['zh'].format(damage)
                print(f"[SPECIAL ATTACK] Damage: {damage} | No shield")
            
            print(f"[STATE] Boss: {self.boss_hp}/{self.boss_max_hp} | Player: {self.player_hp}/{self.player_max_hp} | Shield: {self.shield}")
            
            # Check win/lose conditions
            if self.boss_hp <= 0:
                print(f"\n[WIN] Boss defeated!")
                return "win", result_text
            elif self.player_hp <= 0:
                print(f"\n[LOSE] Player defeated! Final HP: {max(0, self.player_hp)}")
                return "lose", result_text
            
            # Switch back to player turn
            self.current_turn = "player"
            self.cards_played_this_turn = 0
            self.turn += 1
            
            print(f"[TURN] Switched to PLAYER TURN (Turn {self.turn})")
            print(f"=" * 50)
            
            return "playing", result_text
            
        except Exception as e:
            print(f"[ERROR] Exception in _execute_boss_special_attack: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return "playing", T.MSG_ERROR_SPECIAL_ATTACK['zh'].format(e)