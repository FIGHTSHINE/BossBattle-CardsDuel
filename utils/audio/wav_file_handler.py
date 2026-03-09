"""WAV file writing utilities."""

import struct
import wave
from kivy.logger import Logger


class WAVFileHandler:
    """Handle WAV file creation and writing."""
    
    @staticmethod
    def save_wav(filename, samples, sample_rate):
        """
        Save audio samples to WAV file.
        
        Args:
            filename: Output file path
            samples: List of float samples (-1.0 to 1.0)
            sample_rate: Sample rate in Hz
        """
        try:
            # Convert float samples to 16-bit integers
            int_samples = [int(s * 32767) for s in samples]
            
            with wave.open(filename, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                
                # Pack samples
                data = struct.pack('h' * len(int_samples), *int_samples)
                wav_file.writeframes(data)
            
            Logger.info(f"WAVFileHandler: Generated {filename}")
            return True
        except Exception as e:
            Logger.error(f"WAVFileHandler: Failed to save: {e}")
            return False