"""Projectile factory and manager."""

# ✅ 使用相对导入
from .fireball_projectile import FireballProjectile


class ProjectileManager:
    """Manager class for spawning and controlling projectiles."""
    
    @staticmethod
    def create_fireball(start_widget, end_widget, parent_widget, on_hit_complete=None):
        """
        Create a fireball projectile from one widget to another.
        
        Args:
            start_widget: Widget to launch from (e.g., boss_widget)
            end_widget: Widget to target (e.g., player_widget)
            parent_widget: Parent widget to add projectile to
            on_hit_complete: Callback when fireball hits target
            
        Returns:
            FireballProjectile: The created projectile instance
        """
        # Calculate center positions
        start_pos = (
            start_widget.x + start_widget.width / 2,
            start_widget.y + start_widget.height / 2
        )
        
        end_pos = (
            end_widget.x + end_widget.width / 2,
            end_widget.y + end_widget.height / 2
        )
        
        # Create projectile
        projectile = FireballProjectile(
            start_pos=start_pos,
            target_pos=end_pos,
            on_hit_complete=on_hit_complete
        )
        
        # Add to parent widget
        parent_widget.add_widget(projectile)
        
        return projectile