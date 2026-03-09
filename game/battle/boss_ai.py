"""Boss AI and attack system."""

import random
from game.translations import Translations as T


class BossAI:
    """Handles Boss AI decisions and attacks."""
    
    def __init__(self, battle_manager):
        """
        Initialize Boss AI.
        
        Args:
            battle_manager: Reference to BattleManager instance
        """
        self.battle = battle_manager
    
    def decide_action(self):
        """
        Decide Boss's next action.
        
        Returns:
            tuple: (action_type, result_text) where action_type is 'normal' or 'special'
        """
        # Check if boss should use special attack
        boss_hp_percent = self.battle.boss_hp / self.battle.boss_max_hp
        
        if (not self.battle.boss_special_attack_used and 
            boss_hp_percent <= self.battle.boss_special_attack_threshold):
            print(f"[BOSS AI] Deciding: SPECIAL ATTACK")
            print(f"[BOSS AI] Boss HP: {boss_hp_percent*100:.1f}% <= {self.battle.boss_special_attack_threshold*100:.1f}%")
            return 'special', None
        
        print(f"[BOSS AI] Deciding: NORMAL ATTACK")
        return 'normal', None
    
    def execute_normal_attack(self):
        """
        Execute normal boss attack.
        
        Returns:
            tuple: (result, result_text) where result is 'win', 'lose', or 'playing'
        """
        damage = random.randint(self.battle.boss_damage_min, self.battle.boss_damage_max)
        result_text = ""
        self.battle.last_attack_was_special = False
        
        print(f"\n[BOSS ATTACK] Normal attack (damage: {damage}-{self.battle.boss_damage_max})")
        
        # Calculate shield reduction
        if self.battle.shield > 0:
            blocked = min(self.battle.shield, damage)
            actual_damage = damage - blocked
            self.battle.shield -= blocked
            
            # Choose message based on whether player took damage
            if actual_damage > 0:
                self.battle.player_hp -= actual_damage
                result_text = T.MSG_BOSS_ATTACK_BLOCKED_PARTIAL['zh'].format(blocked, actual_damage)
            else:
                result_text = T.MSG_BOSS_ATTACK_BLOCKED['zh'].format(blocked)
            
            print(f"[BOSS ATTACK] Damage: {damage} | Blocked: {blocked} | Actual: {actual_damage}")
        else:
            self.battle.player_hp -= damage
            result_text = T.MSG_BOSS_ATTACK_NO_SHIELD['zh'].format(damage)
            print(f"[BOSS ATTACK] Damage: {damage} | No shield")
        
        print(f"[STATE] Boss: {self.battle.boss_hp}/{self.battle.boss_max_hp} | "
              f"Player: {self.battle.player_hp}/{self.battle.player_max_hp} | "
              f"Shield: {self.battle.shield}")
        
        return self._check_battle_end(result_text)
    
    def execute_special_attack(self):
        """
        Execute boss special attack (90 damage, one-time use).
        
        Returns:
            tuple: (result, result_text) where result is 'win', 'lose', or 'playing'
        """
        print(f"\n{'=' * 50}")
        print(f"[SPECIAL ATTACK] ⚠️ BOSS ENRAGED - SPECIAL ATTACK! ⚠️")
        
        damage = self.battle.boss_special_attack_damage
        result_text = ""
        
        # Mark special attack as used
        self.battle.boss_special_attack_used = True
        self.battle.last_attack_was_special = True
        
        print(f"[SPECIAL ATTACK] Damage: {damage}")
        print(f"[SPECIAL ATTACK] Boss HP: {self.battle.boss_hp}/{self.battle.boss_max_hp} "
              f"({self.battle.boss_hp/self.battle.boss_max_hp*100:.1f}%)")
        
        # Apply damage with shield absorption
        if self.battle.shield > 0:
            blocked = min(self.battle.shield, damage)
            actual_damage = damage - blocked
            self.battle.shield -= blocked
            
            if actual_damage > 0:
                self.battle.player_hp -= actual_damage
                result_text = T.MSG_BOSS_SPECIAL_BLOCKED_PARTIAL['zh'].format(blocked, actual_damage)
            else:
                result_text = T.MSG_BOSS_SPECIAL_BLOCKED['zh'].format(blocked)
            
            print(f"[SPECIAL ATTACK] Damage: {damage} | Blocked: {blocked} | Actual: {actual_damage}")
        else:
            self.battle.player_hp -= damage
            result_text = T.MSG_BOSS_SPECIAL_NO_SHIELD['zh'].format(damage)
            print(f"[SPECIAL ATTACK] Damage: {damage} | No shield")
        
        print(f"[STATE] Boss: {self.battle.boss_hp}/{self.battle.boss_max_hp} | "
              f"Player: {self.battle.player_hp}/{self.battle.player_max_hp} | "
              f"Shield: {self.battle.shield}")
        
        print(f"=" * 50)
        
        return self._check_battle_end(result_text)
    
    def _check_battle_end(self, result_text):
        """
        Check if battle has ended.
        
        Args:
            result_text: Current result text
            
        Returns:
            tuple: (result, result_text) where result is 'win', 'lose', or 'playing'
        """
        # Check win/lose conditions
        if self.battle.boss_hp <= 0:
            print(f"\n[WIN] Boss defeated!")
            return "win", result_text
        elif self.battle.player_hp <= 0:
            print(f"\n[LOSE] Player defeated! Final HP: {max(0, self.battle.player_hp)}")
            return "lose", result_text
        
        return "playing", result_text