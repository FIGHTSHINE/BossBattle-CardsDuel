"""Sound generator - Core coordinator class."""

from .audio.platform_manager import PlatformManager
from .audio.wave_generator import WaveGenerator
from .audio.sound_effects import SoundEffects
from .audio.wav_file_handler import WAVFileHandler
from kivy.logger import Logger


class SoundGenerator:
    """Generate game sound effects programmatically."""
    
    def __init__(self):
        """Initialize sound generator."""
        self.sample_rate = 44100  # CD quality
        self.temp_dir = PlatformManager.get_temp_dir()
        PlatformManager.ensure_temp_dir(self.temp_dir)
        
        Logger.info(f"SoundGenerator: Initialized with temp_dir={self.temp_dir}")
    
    def generate_tone(self, frequency, duration, volume=0.5, wave_type='sine'):
        """
        Generate a simple tone.
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            volume: Volume (0.0 to 1.0)
            wave_type: 'sine', 'square', 'sawtooth', or 'triangle'
        
        Returns:
            str: Path to generated WAV file
        """
        # Generate waveform
        if wave_type == 'sine':
            samples = WaveGenerator.generate_sine_wave(frequency, duration, self.sample_rate)
        elif wave_type == 'square':
            samples = WaveGenerator.generate_square_wave(frequency, duration, self.sample_rate)
        # ... other wave types
        
        # Apply volume
        samples = WaveGenerator.apply_volume(samples, volume)
        
        # Convert to int and save
        filename = f"{self.temp_dir}/tone_{frequency}hz_{wave_type}.wav"
        WAVFileHandler.save_wav(filename, samples, self.sample_rate)
        
        return filename
    
    def generate_victory_fanfare(self):
        """Generate victory fanfare sound effect."""
        samples = SoundEffects.generate_victory_fanfare(self.sample_rate)
        filename = f"{self.temp_dir}/victory_fanfare.wav"
        WAVFileHandler.save_wav(filename, samples, self.sample_rate)
        return filename
    
    def generate_defeat_sound(self):
        """Generate defeat sound effect."""
        samples = SoundEffects.generate_defeat_sound(self.sample_rate)
        filename = f"{self.temp_dir}/defeat_sound.wav"
        WAVFileHandler.save_wav(filename, samples, self.sample_rate)
        return filename
    
    def generate_card_play_sound(self):
        """Generate card play sound effect."""
        samples = SoundEffects.generate_card_play_sound(self.sample_rate)
        filename = f"{self.temp_dir}/card_play.wav"
        WAVFileHandler.save_wav(filename, samples, self.sample_rate)
        return filename
    
    def generate_boss_attack_sound(self):
        """Generate boss attack sound effect."""
        samples = SoundEffects.generate_boss_attack_sound(self.sample_rate)
        filename = f"{self.temp_dir}/boss_attack.wav"
        WAVFileHandler.save_wav(filename, samples, self.sample_rate)
        return filename
    
    def generate_background_music_loop(self):
        """Generate background music loop (calm menu music)."""
        samples = SoundEffects.generate_background_music(self.sample_rate)
        filename = f"{self.temp_dir}/background_music.wav"
        WAVFileHandler.save_wav(filename, samples, self.sample_rate)
        return filename
    
    def generate_battle_music_loop(self):
        """Generate battle music loop (intense combat music)."""
        samples = SoundEffects.generate_battle_music(self.sample_rate)
        filename = f"{self.temp_dir}/battle_music.wav"
        WAVFileHandler.save_wav(filename, samples, self.sample_rate)
        return filename