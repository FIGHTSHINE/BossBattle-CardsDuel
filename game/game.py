"""Data models for the game."""

from dataclasses import dataclass
from enum import Enum


class CardType(Enum):
    """Types of cards in the game."""
    ATTACK = "attack"
    HEAL = "heal"
    SHIELD = "shield"
    CRITICAL = "critical"


@dataclass
class Card:
    """Represents a single card in the game."""
    name: str
    value: int
    card_type: CardType
    color: tuple
    unique_id: int = 0