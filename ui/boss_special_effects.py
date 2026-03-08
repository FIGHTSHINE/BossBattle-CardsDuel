"""Special attack effects for boss."""

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color
from ui.projectile import FireballProjectile


class BossSpecialEffectManager:
    """
    Manager for boss special attack visual effects.
    
    Coordinates the complete special attack sequence:
    1. Boss charging animation (glowing/pulsing)
    2. Projectile launch (fireball)
    3. Impact effects
    4. Callback triggering
    """
    
    def __init__(self):
        """Initialize the special effects manager."""
        self.active_animations = []
    
    def fireball_special_attack(self, boss_widget, player_widget, parent_widget, callback=None):
        """
        Execute complete fireball special attack sequence.
        
        Sequence:
        1. Boss charging animation (0.3s) - pulsing glow
        2. Launch fireball projectile (0.6s flight)
        3. Explosion on impact (0.2s)
        4. Trigger callback
        
        Args:
            boss_widget: Boss widget to launch from
            player_widget: Player widget to target
            parent_widget: Parent widget to add effects to
            callback: Optional callback function when attack completes
            
        Returns:
            None
        """
        # Step 1: Boss charging animation
        self._play_boss_charge_animation(boss_widget)
        
        # Step 2: Schedule fireball launch (after charging completes)
        Clock.schedule_once(
            lambda dt: self._launch_fireball(
                boss_widget, player_widget, parent_widget, callback
            ),
            0.3  # Launch after charge animation
        )
    
    def _play_boss_charge_animation(self, boss_widget):
        """
        Play boss charging/power-up animation.
        
        Boss pulses orange/red to indicate charging special attack.
        
        Args:
            boss_widget: Boss widget to animate
        """
        # Store original state if available
        original_opacity = boss_widget.opacity
        original_scale = getattr(boss_widget, 'scale', 1.0)
        
        # Create pulsing effect (scale up + glow)
        # Animation sequence: expand → contract → repeat
        pulse_expand = Animation(
            opacity=1.0,
            duration=0.15,
            t='out_quad'
        )
        
        pulse_contract = Animation(
            opacity=0.7,
            duration=0.15,
            t='in_quad'
        )
        
        # Store reference to animation for cleanup
        charge_anim = pulse_expand + pulse_contract
        charge_anim.start(boss_widget)
        self.active_animations.append(charge_anim)
        
        # Additionally, we could modify boss aura color if renderer supports it
        # This is optional enhancement if boss_renderer has aura_color property
        if hasattr(boss_widget, 'renderer') and hasattr(boss_widget.renderer, 'canvas_instructions'):
            aura_color_key = 'aura_color'
            if aura_color_key in boss_widget.renderer.canvas_instructions:
                # Change aura to orange/red to indicate charging
                original_aura = boss_widget.renderer.canvas_instructions[aura_color_key].rgba
                boss_widget.renderer.canvas_instructions[aura_color_key].rgba = (1.0, 0.4, 0.0, 0.6)
                
                # Schedule restoration after charge completes
                def restore_aura(dt):
                    boss_widget.renderer.canvas_instructions[aura_color_key].rgba = original_aura
                
                Clock.schedule_once(restore_aura, 0.3)
    
    def _launch_fireball(self, boss_widget, player_widget, parent_widget, callback):
        """
        Launch fireball projectile from boss to player.
        
        Args:
            boss_widget: Boss widget (launch position)
            player_widget: Player widget (target position)
            parent_widget: Parent widget to add projectile to
            callback: Callback when fireball hits
        """
        # ✅ FIX: Use widget.center to get center coordinates
        # Then convert to parent's coordinate system
        boss_center_local = (boss_widget.center_x, boss_widget.center_y)
        player_center_local = (player_widget.center_x, player_widget.center_y)
        
        # Convert to parent coordinates (parent is game_screen)
        boss_center = boss_widget.to_parent(*boss_center_local)
        player_center = player_widget.to_parent(*player_center_local)
        
        # Debug: Print coordinates
        print(f"[FIREBALL] Boss widget center: {boss_center_local}")
        print(f"[FIREBALL] Boss in parent coords: {boss_center}")
        print(f"[FIREBALL] Player widget center: {player_center_local}")
        print(f"[FIREBALL] Player in parent coords: {player_center}")
        print(f"[FIREBALL] Distance: ({player_center[0]-boss_center[0]:.1f}, {player_center[1]-boss_center[1]:.1f})")
        
        # Create fireball
        fireball = FireballProjectile(
            start_pos=boss_center,
            target_pos=player_center,
            on_hit_complete=lambda _: self._on_fireball_hit(player_widget, callback)
        )
        
        # Add fireball to parent widget
        parent_widget.add_widget(fireball, index=0)  # index=0 = top of stack
        print(f"[FIREBALL] Added to parent at index 0 (top layer)")
        
        # Store reference for cleanup (optional)
        self.active_animations.append(fireball)
    
    def _on_fireball_hit(self, player_widget, callback):
        """
        Handle fireball impact with player.
        
        Args:
            player_widget: Player widget that was hit
            callback: Optional callback to trigger
        """
        # Trigger player hit animation (shake + red flash)
        if player_widget and hasattr(player_widget, 'animations'):
            player_widget.animations.hit_animation()
        
        # Trigger user callback if provided
        if callback:
            callback()
    
    def clear_all_animations(self):
        """
        Stop and clear all active animations.
        
        Useful for cleanup when game is reset or special attack is interrupted.
        """
        for anim in self.active_animations:
            if hasattr(anim, 'cancel'):
                anim.cancel(self)
        
        self.active_animations.clear()
    
    def alternative_special_attack(self, attack_type, boss_widget, player_widget, parent_widget, callback=None):
        """
        Placeholder for future special attack types.
        
        This method allows easy extension with different attack patterns
        without modifying the existing fireball attack.
        
        Future examples:
        - 'shadow_wave': Expanding dark circle from boss
        - 'multi_projectile': Multiple small projectiles
        - 'beam_attack': Continuous laser beam
        
        Args:
            attack_type: String identifier for attack type
            boss_widget: Boss widget
            player_widget: Player widget
            parent_widget: Parent widget for effects
            callback: Completion callback
        """
        # Future implementation
        if attack_type == 'shadow_wave':
            # TODO: Implement shadow wave attack
            pass
        elif attack_type == 'multi_projectile':
            # TODO: Implement multi-projectile attack
            pass
        elif attack_type == 'beam_attack':
            # TODO: Implement beam attack
            pass
        else:
            # Default to fireball
            self.fireball_special_attack(boss_widget, player_widget, parent_widget, callback)