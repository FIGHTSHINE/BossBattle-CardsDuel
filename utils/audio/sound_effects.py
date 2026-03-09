"""Game sound effect generators."""

import math
from .wave_generator import WaveGenerator


class SoundEffects:
    """Generate various game sound effects."""
    
    @staticmethod
    def generate_victory_fanfare(sample_rate):
        """Generate victory fanfare (ascending arpeggio)."""
        # Arpeggio: C5, E5, G5, C6
        notes = [
            WaveGenerator.NOTE_C5,
            WaveGenerator.NOTE_E5,
            WaveGenerator.NOTE_G5,
            WaveGenerator.NOTE_C6
        ]
        
        samples = []
        note_duration = 0.15
        
        for freq in notes:
            # Generate sine wave for this note
            note_samples = WaveGenerator.generate_sine_wave(freq, note_duration, sample_rate)
            
            # Apply envelope
            note_samples = WaveGenerator.apply_envelope(note_samples, sample_rate, 0.1, 0.3)
            note_samples = WaveGenerator.apply_volume(note_samples, 0.5)
            
            samples.extend(note_samples)
        
        return samples
    
    @staticmethod
    def generate_defeat_sound(sample_rate):
        """Generate defeat sound (descending tone)."""
        duration = 1.0
        num_samples = int(sample_rate * duration)
        samples = []
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            
            # Descending frequency: 300Hz → 100Hz
            freq = 300.0 - (200.0 * t)
            
            # Add vibrato
            vibrato = 1.0 + 0.05 * math.sin(2 * math.pi * 5.0 * t)
            
            value = math.sin(2 * math.pi * freq * vibrato * t) * 0.4
            
            # Fade out
            envelope = 1.0 - t
            value *= envelope
            
            # Clamp value to [-1.0, 1.0] to prevent WAV conversion errors
            clamped_value = max(-1.0, min(1.0, value))
            samples.append(clamped_value)
        
        return samples
    
    @staticmethod
    def generate_card_play_sound(sample_rate):
        """
        Generate POWERFUL card play sound.
        
        Sounds like a gun shot or punchy drum hit!
        """
        duration = 0.3
        num_samples = int(sample_rate * duration)
        samples = []
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            
            # 💥 Layer 1: Deep bass punch (thump)
            bass_kick = 0.35 * math.sin(2 * math.pi * 100.0 * t)  # ✅ 进一步降低到 0.35
            
            # 🔫 Layer 2: Sharp transient (gun shot crack)
            if t < 0.05:
                # High-frequency noise burst for "crack"
                noise = (hash(int(t * 10000)) % 1000) / 500.0 - 1.0
                transient = noise * 0.3 * math.exp(-t * 100.0)  # ✅ 降低到 0.3
            else:
                transient = 0.0
            
            # 🥁 Layer 3: Mid punch (body of sound)
            mid_punch = 0.2 * math.sin(2 * math.pi * 200.0 * t)  # ✅ 降低到 0.2
            
            # 🔊 Layer 4: Square wave for punchiness
            square = 0.15 * (1.0 if math.sin(2 * math.pi * 150.0 * t) >= 0 else -1.0)  # ✅ 降低到 0.15
            
            # Mix all layers
            value = bass_kick + transient + mid_punch + square  # 最大 1.0（安全范围）
            
            # ✅ Punchy ADSR envelope (fast attack, medium decay)
            if t < 0.01:
                envelope = t / 0.01
            elif t < 0.15:
                envelope = 1.0 - ((t - 0.01) / 0.14) * 0.7
            else:
                envelope = 0.3 * math.exp(-(t - 0.15) * 15.0)
            
            value *= envelope
            
            # 双重保护：hard clamp + small epsilon
            clamped_value = max(-0.999, min(0.999, value))  # ✅ 留出微小边距
            samples.append(clamped_value)
    
        return samples
    
    @staticmethod
    def generate_boss_attack_sound(sample_rate):
        """Generate boss attack sound (deep rumble)."""
        duration = 0.5
        num_samples = int(sample_rate * duration)
        samples = []
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            
            # Low frequency oscillator (reduced to prevent clipping)
            value = math.sin(2 * math.pi * 80.0 * t) * 0.6  # ✅ 1.2 → 0.6
            
            # Add harmonics (also reduced)
            value += 0.35 * math.sin(2 * math.pi * 120.0 * t)  # ✅ 0.7 → 0.35
            value += 0.25 * math.sin(2 * math.pi * 160.0 * t)  # ✅ 0.5 → 0.25
            
            # Decay envelope (slower decay for more impact)
            envelope = math.exp(-t * 3.0)
            value *= envelope
            
            # ✅ 添加 clamping 保护
            clamped_value = max(-0.999, min(0.999, value))
            samples.append(clamped_value)
    
        return samples
    
    @staticmethod
    def generate_background_music(sample_rate):
        """Generate background music loop (epic chord progression)."""
        duration = 8.0
        
        # Chord progression: Am - F - C - G
        chords = [
            [220.0, 277.18, 329.63],  # Am
            [174.61, 220.0, 261.63],  # F
            [261.63, 329.63, 392.0],  # C
            [196.0, 246.94, 293.66],  # G
        ]
        
        samples = []
        samples_per_chord = int(sample_rate * duration / len(chords))
        
        for chord_idx, chord in enumerate(chords):
            for i in range(samples_per_chord):
                t = float(i) / sample_rate
                
                # Mix chord frequencies
                value = 0.0
                for freq in chord:
                    value += math.sin(2 * math.pi * freq * t)
                
                # Normalize
                value *= 0.15
                
                # Add subtle rhythm
                beat = int(t * 2) % 2
                value *= (0.8 if beat == 0 else 0.6)
                
                # Smooth chord transition
                transition_samples = int(sample_rate * 0.1)
                if i < transition_samples and chord_idx > 0:
                    factor = i / transition_samples
                    value = value * factor
                
                samples.append(value)
        
        return samples

    @staticmethod
    def generate_battle_music(sample_rate):
        """
        Generate NES-style battle music (Contra/Double Dragon style).
        
        Features:
        - Clear melody line (not ambient)
        - Square wave for melody, triangle wave for bass
        - Fast bassline (eighth notes)
        - Simple kick-snare drum pattern
        - Energy builds up (low to high)
        """
        bpm = 150  # Classic game tempo
        duration = 8.0  # 8 seconds for full loop
    
        # 🎵 MELODY: Clear, memorable tune (eighth notes)
        # Based on pentatonic scale for heroic feel
        melody_notes = [
            # A段 (bars 1-4) - Main theme
            440.00, 523.25, 587.33, 440.00,  # A C# D A (heroic上升)
            392.00, 440.00, 493.88, 523.25,  # G A B C# (building)
            587.33, 659.25, 587.33, 440.00,  # D E D A (tension)
            392.00, 349.23, 392.00, 440.00,  # G F G A (resolve)
            
            # B段 (bars 5-8) - Higher energy
            523.25, 587.33, 659.25, 783.99,  # C# D E G (climax!)
            659.25, 587.33, 523.25, 440.00,  # E D C# A (falling)
            392.00, 440.00, 493.88, 523.25,  # G A B C# (rebuild)
            587.33, 659.25, 587.33, 440.00,  # D E D A (final)
        ]
        
        # 🎸 BASSLINE: Fast eighth notes, driving rhythm
        bass_notes = [
            55.00, 55.00, 65.41, 65.41,  # A1 A1 C2 C2 (pumping)
            73.42, 73.42, 82.41, 82.41,  # D2 D2 E2 E2 (ascending)
            55.00, 55.00, 65.41, 65.41,  # Repeat A1
            73.42, 73.42, 82.41, 82.41,  # Repeat D2
            
            55.00, 55.00, 65.41, 65.41,  # Same pattern
            73.42, 73.42, 82.41, 82.41,
            55.00, 55.00, 65.41, 65.41,
            73.42, 73.42, 82.41, 82.41,
        ]
        
        # Calculate timing
        total_notes = len(melody_notes)
        samples_per_note = int(sample_rate * duration / total_notes)
        beat_duration = 60.0 / bpm
        samples_per_beat = int(sample_rate * beat_duration)
        
        samples = []
        melody_idx = 0
        bass_idx = 0
        
        for note_idx in range(total_notes):
            for i in range(samples_per_note):
                t_global = (note_idx * samples_per_note + i) / sample_rate
            
                # 🎵 MELODY: Square wave (classic NES sound)
                melody_freq = melody_notes[note_idx % len(melody_notes)]
                # Square wave for melody
                melody_wave = 1.0 if math.sin(2 * math.pi * melody_freq * t_global) >= 0 else -1.0
                melody = melody_wave * 0.15  # Moderate volume
            
                # 🎸 BASS: Triangle wave (softer, punchy)
                bass_freq = bass_notes[note_idx % len(bass_notes)]
                # Triangle wave approximation
                bass_phase = (t_global * bass_freq) % 1.0
                triangle = 2.0 * abs(2.0 * bass_phase - 1.0) - 1.0
                bass = triangle * 0.12  # Lower volume
            
                # 💥 DRUMS: Simple kick-snare pattern
                beat = int(t_global / beat_duration) % 4
                drum = 0.0
            
                if beat == 0 or beat == 2:
                    # Kick drum (low sine)
                    kick = 0.3 * math.sin(2 * math.pi * 80.0 * t_global)
                    drum += kick
                elif beat == 1 or beat == 3:
                    # Snare (noise burst)
                    snare = 0.15 * (1.0 if (hash(int(t_global * 1000)) % 2) else -1.0)
                    drum += snare
            
                # Hi-hat on off-beats (optional)
                if i % (samples_per_beat // 2) == 0 and beat % 2 == 1:
                    hihat = 0.05 * (1.0 if math.sin(2 * math.pi * 1000.0 * t_global) >= 0 else -1.0)
                    drum += hihat
            
                # 🔊 Mix all layers
                value = melody + bass + drum
            
                # Quick attack/release for each note (NES style)
                envelope_length = min(samples_per_note // 4, 500)
                if i < envelope_length:
                    # Attack
                    factor = i / envelope_length
                    value *= factor
                elif i > samples_per_note - envelope_length:
                    # Release
                    factor = (samples_per_note - i) / envelope_length
                    value *= factor
            
                # Normalize
                clamped_value = max(-1.0, min(1.0, value))
                samples.append(clamped_value)
    
        return samples