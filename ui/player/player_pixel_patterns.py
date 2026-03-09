"""Pixel art patterns for player character."""

# Body pixel pattern (7x6 grid)
BODY_PATTERN = [
    [0, 1, 1, 1, 1, 0],  # Head row
    [0, 1, 1, 1, 1, 0],  # Head row
    [1, 1, 1, 1, 1, 1],  # Chest row
    [1, 1, 1, 1, 1, 1],  # Chest row
    [1, 1, 1, 1, 1, 1],  # Chest row
    [0, 1, 1, 1, 1, 0],  # Waist row
    [0, 0, 1, 1, 0, 0],  # Legs row
]

# Sword pixel pattern (7x3 grid)
SWORD_PATTERN = [
    [0, 0, 1],  # Tip
    [0, 1, 1],  # Blade
    [0, 1, 1],  # Blade
    [0, 1, 1],  # Blade
    [1, 1, 1],  # Guard
    [1, 0, 1],  # Guard
    [0, 1, 0],  # Handle
]

# Shield pixel pattern (4x4 grid)
SHIELD_PATTERN = [
    [0, 1, 1, 0],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [0, 1, 1, 0],
]

# Cape pixel pattern (5x3 grid)
CAPE_PATTERN = [
    [1, 0, 1],
    [1, 0, 1],
    [1, 0, 1],
    [1, 0, 1],
    [0, 1, 0],
]

# Color definitions
BODY_COLORS = {
    'normal': (0.2, 0.8, 0.3, 1),    # Green
    'damaged': (0.9, 0.6, 0.2, 1),  # Orange
    'critical': (0.9, 0.2, 0.2, 1),  # Red
}

AURA_COLORS = {
    'normal': (0.2, 0.8, 0.3, 0.3),  # Green
    'damaged': (0.9, 0.6, 0.2, 0.4),  # Orange
    'critical': (0.9, 0.2, 0.2, 0.5), # Red
}

EYE_COLORS = {
    'normal': (1, 1, 1, 1),      # White
    'damaged': (1, 0.8, 0.5, 1), # Yellowish
    'critical': (1, 0.3, 0.3, 1),# Reddish
}

CAPE_COLORS = {
    'normal': (0.1, 0.3, 0.6, 1),   # Dark blue
    'damaged': (0.4, 0.2, 0.5, 1),  # Purple
    'critical': (0.5, 0.1, 0.1, 1),  # Dark red
}

SWORD_COLORS = {
    'normal': (0.9, 0.9, 0.9, 1),    # Silver
    'attacking': (1, 1, 0.5, 1),     # Glowing yellow
}

SHIELD_COLOR = (0.3, 0.5, 0.8, 1)  # Blue shield