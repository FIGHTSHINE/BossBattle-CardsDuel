"""Audio waveform generation utilities."""

import math


class WaveGenerator:
    """Generate various audio waveforms."""
    
    # Note frequencies (Hz)
    NOTE_C4 = 261.63
    NOTE_D4 = 293.66
    NOTE_E4 = 329.63
    NOTE_F4 = 349.23
    NOTE_G4 = 392.00
    NOTE_A4 = 440.00
    NOTE_B4 = 493.88
    NOTE_C5 = 523.25
    NOTE_E5 = 659.25
    NOTE_G5 = 783.99
    NOTE_C6 = 1046.50
    
    @staticmethod
    def generate_sine_wave(frequency, duration, sample_rate):
        """Generate sine wave samples."""
        num_samples = int(sample_rate * duration)
        samples = []
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            value = math.sin(2 * math.pi * frequency * t)
            samples.append(value)
        
        return samples
    
    @staticmethod
    def generate_square_wave(frequency, duration, sample_rate):
        """Generate square wave samples."""
        num_samples = int(sample_rate * duration)
        samples = []
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            value = 1.0 if math.sin(2 * math.pi * frequency * t) > 0 else -1.0
            samples.append(value)
        
        return samples
    
    @staticmethod
    def apply_volume(samples, volume):
        """Apply volume to samples."""
        return [s * volume for s in samples]
    
    @staticmethod
    def apply_envelope(samples, sample_rate, attack=0.1, decay=0.3):
        """Apply ADSR envelope to samples."""
        total_samples = len(samples)
        attack_samples = int(total_samples * attack)
        decay_samples = int(total_samples * decay)
        
        result = []
        for i, sample in enumerate(samples):
            if i < attack_samples:
                envelope = i / attack_samples
            elif i > total_samples - decay_samples:
                envelope = (total_samples - i) / decay_samples
            else:
                envelope = 1.0
            
            result.append(sample * envelope)
        
        return result