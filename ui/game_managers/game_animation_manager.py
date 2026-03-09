"""Game animation coordination manager."""

from kivy.app import App
from game.models import CardType


class GameAnimationManager:
    """Manages all game animations and visual effects."""
    
    def __init__(self, stats_display):
        """
        Initialize animation manager.
        
        Args:
            stats_display: StatsDisplay instance containing boss/player widgets
        """
        self.stats_display = stats_display
        self.boss_widget = stats_display.boss_widget
        self.player_widget = stats_display.player_widget
    
    def play_card_animation(self, card):
        """
        Play animation based on card type.
        
        Args:
            card: Card object being played
        """
        if card.card_type in [CardType.ATTACK, CardType.CRITICAL]:
            self._play_attack_animation()
        elif card.card_type == CardType.HEAL:
            self._play_heal_animation()
        # Shield cards don't need animation
    
    def _play_attack_animation(self):
        """Play attack animation (boss hit, player attack)."""
        if self.boss_widget:
            self.boss_widget.hit_animation()
        if self.player_widget:
            self.player_widget.attack_animation()
    
    def _play_heal_animation(self):
        """Play heal animation."""
        if self.player_widget:
            self.player_widget.heal_animation()
    
    def play_boss_attack_animation(self, is_special, callback):
        """
        Play boss attack animation.
        
        Args:
            is_special: Whether this is a special attack
            callback: Function to call after animation completes
        """
        if is_special:
            self._play_special_attack_animation(callback)
        else:
            self._play_normal_attack_animation(callback)
    
    def _play_normal_attack_animation(self, callback):
        """
        Play normal boss attack animation.
        
        Args:
            callback: Function to call after animation
        """
        if self.boss_widget:
            self.boss_widget.attack_animation()
        if self.player_widget:
            self.player_widget.hit_animation()
        
        # Call callback immediately (normal attacks are instant)
        if callback:
            callback()
    
    def _play_special_attack_animation(self, callback):
        """
        Play boss special attack animation (fireball projectile).
        
        Args:
            callback: Function to call after animation completes
        """
        if self.boss_widget and self.player_widget:
            boss_anim = self.boss_widget.animations
            # Special attack animation will call callback when complete
            # This requires passing the parent widget (GameScreen)
            # We'll handle this in the TurnEventHandler
            return True  # Signal that async animation started
        return False
    
    def play_player_hit_animation(self):
        """Play player being hit animation."""
        if self.player_widget:
            self.player_widget.hit_animation()
    
    def play_boss_hit_animation(self):
        """Play boss being hit animation."""
        if self.boss_widget:
            self.boss_widget.hit_animation()