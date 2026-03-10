"""Card effect handlers for battle system."""

from game.translations import Translations as T
import random


class CardEffectHandler:
    """Handles all card effects during battle."""
    
    @staticmethod
    def apply_attack_card(battle, card):
        """
        Apply attack card effect.
        
        Args:
            battle: BattleManager instance
            card: Card object to apply
            
        Returns:
            tuple: (result_text, damage_dealt)
        """
        boss_hp_before = battle.boss_hp
        # ✅ 限制最小值为 0
        battle.boss_hp = max(0, battle.boss_hp - card.value)
        damage_dealt = card.value
        
        result_text = f"Used {card.name}! Dealt {card.value} damage!"
        print(f"[EFFECT] Attack: Boss HP {boss_hp_before} → {battle.boss_hp}")
        
        return result_text, damage_dealt
    
    @staticmethod
    def apply_critical_card(battle, card):
        """
        Apply critical card effect with 20% chance for double damage.
        
        Args:
            battle: BattleManager instance
            card: Card object to apply
            
        Returns:
            tuple: (result_text, damage_dealt)
        """
        boss_hp_before = battle.boss_hp
        
        # 20% chance for double damage
        if random.random() < 0.2:
            damage = card.value * 2
            # ✅ 限制最小值为 0
            battle.boss_hp = max(0, battle.boss_hp - damage)
            result_text = f"CRITICAL HIT! {card.name} deals {damage} damage!"
            print(f"[EFFECT] CRITICAL HIT! Boss HP {boss_hp_before} → {battle.boss_hp}")
        else:
            damage = card.value
            # ✅ 限制最小值为 0
            battle.boss_hp = max(0, battle.boss_hp - damage)
            result_text = f"Used {card.name}! Dealt {card.value} damage!"
            print(f"[EFFECT] Attack: Boss HP {boss_hp_before} → {battle.boss_hp}")
        
        return result_text, damage
    
    @staticmethod
    def apply_heal_card(battle, card):
        """
        Apply heal card effect.
        
        Args:
            battle: BattleManager instance
            card: Card object to apply
            
        Returns:
            tuple: (result_text, heal_amount)
        """
        player_hp_before = battle.player_hp
        heal_amount = min(card.value, battle.player_max_hp - battle.player_hp)
        battle.player_hp += heal_amount
        
        result_text = f"Healed {heal_amount} HP!"
        print(f"[EFFECT] Heal: Player HP {player_hp_before} → {battle.player_hp}")
        
        return result_text, heal_amount
    
    @staticmethod
    def apply_shield_card(battle, card):
        """
        Apply shield card effect.
        
        Args:
            battle: BattleManager instance
            card: Card object to apply
            
        Returns:
            tuple: (result_text, shield_value)
        """
        battle.shield = card.value
        result_text = T.MSG_SHIELD_UP['zh'].format(card.value)
        
        print(f"[EFFECT] Shield: Shield value set to {battle.shield}")
        
        return result_text, card.value
    
    @staticmethod
    def apply_card(battle, card):
        """
        Apply any card effect based on its type.
        
        Args:
            battle: BattleManager instance
            card: Card object to apply
            
        Returns:
            tuple: (result_text, value_applied)
        """
        card_type = card.card_type.value
        
        if card_type == "attack":
            return CardEffectHandler.apply_attack_card(battle, card)
        elif card_type == "critical":
            return CardEffectHandler.apply_critical_card(battle, card)
        elif card_type == "heal":
            return CardEffectHandler.apply_heal_card(battle, card)
        elif card_type == "shield":
            return CardEffectHandler.apply_shield_card(battle, card)
        else:
            print(f"[WARNING] Unknown card type: {card_type}")
            return f"Used {card.name}", 0