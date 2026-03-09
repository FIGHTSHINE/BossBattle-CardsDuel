"""Projectile effects - Backward compatibility wrapper."""

# Re-export for backward compatibility
from .projectiles.fireball_projectile import FireballProjectile
from .projectiles.projectile_manager import ProjectileManager

__all__ = ['FireballProjectile', 'ProjectileManager']