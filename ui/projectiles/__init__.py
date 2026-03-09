"""Projectiles module - Visual effects for boss attacks."""

# Export all projectile classes
from .fireball_projectile import FireballProjectile
from .fireball_graphics import FireballGraphics
from .fireball_animation import FireballAnimation
from .projectile_manager import ProjectileManager

__all__ = [
    'FireballProjectile',
    'FireballGraphics',
    'FireballAnimation',
    'ProjectileManager'
]