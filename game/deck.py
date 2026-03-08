"""Card deck creation and management."""

from game.models import Card, CardType
from game.translations import language_manager


class Deck:
    """Deck management class."""
    
    @staticmethod
    def create_balanced_deck():
        """
        Create a balanced deck with various card types.
        
        Returns:
            list: List of Card objects
        """
        # Get current language
        lang = language_manager.current_language
        
        # Define card names in both languages
        if lang == 'zh':
            attack_names = [
                ("普通攻击", "Common Attack"),
                ("重击", "Heavy Strike"),
                ("强力斩击", "Power Slash"),
                ("快速打击", "Quick Strike"),
                ("连击", "Combo"),
                ("终结技", "Finisher")
            ]
            
            heal_names = [
                ("小治疗", "Small Heal"),
                ("中治疗", "Medium Heal"),
                ("大治疗", "Big Heal")
            ]
            
            shield_names = [
                ("木盾", "Wood Shield"),
                ("铁盾", "Iron Shield"),
                ("钻石盾", "Diamond Shield")
            ]
            
            critical_names = [
                ("致命一击", "Critical Hit"),
                ("雷霆一击", "Thunder Strike")
            ]
        else:  # English
            attack_names = [
                ("Common Attack", "Common Attack"),
                ("Heavy Strike", "Heavy Strike"),
                ("Power Slash", "Power Slash"),
                ("Quick Strike", "Quick Strike"),
                ("Combo", "Combo"),
                ("Finisher", "Finisher")
            ]
            
            heal_names = [
                ("Small Heal", "Small Heal"),
                ("Medium Heal", "Medium Heal"),
                ("Big Heal", "Big Heal")
            ]
            
            shield_names = [
                ("Wood Shield", "Wood Shield"),
                ("Iron Shield", "Iron Shield"),
                ("Diamond Shield", "Diamond Shield")
            ]
            
            critical_names = [
                ("Critical Hit", "Critical Hit"),
                ("Thunder Strike", "Thunder Strike")
            ]
        
        deck = []
        
        # 攻击卡 (10张) - Attack cards (10)
        deck.extend([
            Card(attack_names[0][0], 10, CardType.ATTACK, (0.8, 0.3, 0.3, 1)),
            Card(attack_names[0][0], 10, CardType.ATTACK, (0.8, 0.3, 0.3, 1)),
            Card(attack_names[0][0], 10, CardType.ATTACK, (0.8, 0.3, 0.3, 1)),
            Card(attack_names[1][0], 15, CardType.ATTACK, (0.9, 0.2, 0.2, 1)),
            Card(attack_names[1][0], 30, CardType.ATTACK, (0.9, 0.2, 0.2, 1)),
            Card(attack_names[2][0], 40, CardType.ATTACK, (1, 0.1, 0.1, 1)),
            Card(attack_names[3][0], 30, CardType.ATTACK, (0.7, 0.4, 0.4, 1)),
            Card(attack_names[3][0], 12, CardType.ATTACK, (0.7, 0.4, 0.4, 1)),
            Card(attack_names[4][0], 50, CardType.ATTACK, (0.85, 0.25, 0.25, 1)),
            Card(attack_names[5][0], 60, CardType.ATTACK, (1, 0, 0, 1)),
        ])
        
        # 治疗卡 (4张) - Heal cards (4)
        deck.extend([
            Card(heal_names[0][0], 10, CardType.HEAL, (0.3, 0.8, 0.3, 1)),
            Card(heal_names[0][0], 10, CardType.HEAL, (0.3, 0.8, 0.3, 1)),
            Card(heal_names[1][0], 15, CardType.HEAL, (0.2, 1, 0.5, 1)),
            Card(heal_names[2][0], 25, CardType.HEAL, (0.1, 1, 0.3, 1)),
        ])
        
        # 护盾卡 (3张) - Shield cards (3)
        deck.extend([
            Card(shield_names[0][0], 5, CardType.SHIELD, (0.3, 0.6, 1, 1)),
            Card(shield_names[1][0], 8, CardType.SHIELD, (0.2, 0.5, 0.9, 1)),
            Card(shield_names[2][0], 12, CardType.SHIELD, (0.1, 0.4, 0.8, 1)),
        ])
        
        # 暴击卡 (3张) - Critical cards (3)
        deck.extend([
            Card(critical_names[0][0], 10, CardType.CRITICAL, (0.9, 0.3, 1, 1)),
            Card(critical_names[0][0], 10, CardType.CRITICAL, (0.9, 0.3, 1, 1)),
            Card(critical_names[1][0], 30, CardType.CRITICAL, (0.95, 0.2, 0.95, 1)),
        ])
        
        return deck