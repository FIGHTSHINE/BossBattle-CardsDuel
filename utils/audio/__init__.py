"""Audio generation module."""

from .platform_manager import PlatformManager
from .wave_generator import WaveGenerator
from .sound_effects import SoundEffects
from .wav_file_handler import WAVFileHandler

__all__ = [
    'PlatformManager',
    'WaveGenerator',
    'SoundEffects',
    'WAVFileHandler'
]