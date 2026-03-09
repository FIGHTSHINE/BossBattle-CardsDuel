"""Audio manager for background music and sound effects."""

from kivy.core.audio import SoundLoader
from kivy.logger import Logger
from kivy.clock import Clock
import os


class AudioManager:
    """Singleton audio manager for the game."""
    
    _instance = None
    
    def __new__(cls):
        """Ensure singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize audio manager."""
        if self._initialized:
            return
        
        self._initialized = True
        
        # Audio settings
        self.music_volume = 0.4   # ✅ 正确：使用普通数值
        self.sfx_volume = 0.7     # ✅ 正确：使用普通数值
        self.muted = False        # ✅ 正确：使用普通布尔值
        
        # Audio objects - Multiple background music tracks
        self.menu_music = None          # Calm menu music
        self.battle_music = None         # Intense battle music
        self.current_music = None        # Currently playing music
        self.sound_effects = {}
        
        # Sound file paths (will be set later)
        self.sound_files = {
            'victory': None,
            'defeat': None,
            'card_play': None,
            'boss_attack': None,
            'menu_music': None,          # Renamed from 'background_music'
            'battle_music': None,        # ✅ New: Battle music track
        }
        
        Logger.info("AudioManager: Initialized")
    
    def set_sound_file(self, name, filepath):
        """
        Register a sound file.
        
        Args:
            name: Sound name ('victory', 'defeat', etc.)
            filepath: Path to audio file
        """
        self.sound_files[name] = filepath
        Logger.info(f"AudioManager: Registered sound '{name}': {filepath}")
    
    def load_sounds(self):
        """Load all sound effects into memory."""
        for name, filepath in self.sound_files.items():
            if filepath and os.path.exists(filepath):
                try:
                    sound = SoundLoader.load(filepath)
                    if sound:
                        sound.volume = self.music_volume if name in ('menu_music', 'battle_music') else self.sfx_volume
                        self.sound_effects[name] = sound
                        # ✅ Add detailed logging for music files
                        if name in ('menu_music', 'battle_music'):
                            Logger.info(f"AudioManager: Loaded sound '{name}' from: {filepath} (id: {id(sound)})")
                        else:
                            Logger.info(f"AudioManager: Loaded sound '{name}'")
                    else:
                        Logger.warning(f"AudioManager: Failed to load sound '{name}'")
                except Exception as e:
                    Logger.error(f"AudioManager: Error loading '{name}': {e}")
    
    def play_background_music(self, loop=True):
        """Start background music playback."""
        if self.muted:
            return
        
        if 'background_music' in self.sound_effects:
            self.background_music = self.sound_effects['background_music']
            
            if self.background_music:
                self.background_music.loop = loop
                self.background_music.volume = self.music_volume
                self.background_music.play()
                Logger.info("AudioManager: Background music started")
        else:
            Logger.warning("AudioManager: No background music loaded")
    
    def stop_background_music(self):
        """Stop background music playback."""
        if self.current_music and self.current_music.state == 'play':
            self.current_music.stop()
            Logger.info("AudioManager: Background music stopped")
    
    def play_sound(self, name):
        """
        Play a sound effect.
        
        Args:
            name: Sound name ('victory', 'defeat', 'card_play', 'boss_attack')
        """
        if self.muted:
            return
        
        if name in self.sound_effects:
            sound = self.sound_effects[name]
            if sound:
                sound.volume = self.sfx_volume
                
                # Stop previous playback if any
                if sound.state == 'play':
                    sound.stop()
                
                sound.play()
                Logger.info(f"AudioManager: Playing sound '{name}'")
        else:
            Logger.warning(f"AudioManager: Sound '{name}' not found")
    
    def toggle_mute(self):
        """Toggle mute on/off."""
        self.muted = not self.muted
        
        if self.muted:
            # Stop all audio
            self.stop_all_music()  # ✅ 使用新方法
            for sound in self.sound_effects.values():
                if sound and sound.state == 'play':
                    sound.stop()
            Logger.info("AudioManager: Muted")
        else:
            # Resume background music
            if self.menu_music:
                self.play_menu_music()
            Logger.info("AudioManager: Unmuted")
        
        return self.muted
    
    def set_music_volume(self, volume):
        """
        Set background music volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        
        if self.current_music:
            self.current_music.volume = self.music_volume
    
    def set_sfx_volume(self, volume):
        """
        Set sound effects volume.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def cleanup(self):
        """Release all audio resources."""
        self.stop_all_music()
        
        for sound in self.sound_effects.values():
            if sound:
                sound.unload()
        
        self.sound_effects.clear()
        Logger.info("AudioManager: Cleaned up")

    def play_menu_music(self, loop=True):
        """Start menu music playback (calm background music)."""
        if self.muted:
            return
    
        if 'menu_music' in self.sound_effects:
            # Mute current music instead of stopping (Windows fix)
            if self.current_music:
                self.current_music.volume = 0.0
            
            self.menu_music = self.sound_effects['menu_music']
            self.current_music = self.menu_music
            
            if self.menu_music:
                self.menu_music.loop = loop
                self.menu_music.volume = self.music_volume
                self.menu_music.play()
                Logger.info("AudioManager: Menu music started")
            else:
                Logger.error("AudioManager: menu_music object is None!")
        else:
            Logger.warning("AudioManager: No menu_music loaded")

    def play_battle_music(self, loop=True):
        """Start battle music playback (intense combat music)."""
        if self.muted:
            return
    
        if 'battle_music' in self.sound_effects:
            # ✅ Instead of stopping, mute the current music
            if self.current_music:
                Logger.info(f"AudioManager: Muting current music (id: {id(self.current_music)})")
                self.current_music.volume = 0.0  # ✅ Mute instead of stop
                Logger.info("AudioManager: Current music muted")
            
            # ✅ Load battle music from file
            battle_music_file = self.sound_files['battle_music']
            from kivy.core.audio import SoundLoader#type: ignore Import here to avoid circular import issues
            self.battle_music = SoundLoader.load(battle_music_file)
            
            if self.battle_music:
                self.battle_music.loop = loop
                self.battle_music.volume = self.music_volume
                self.battle_music.play()
                self.current_music = self.battle_music
                Logger.info(f"AudioManager: Battle music started with volume {self.music_volume}")
                Logger.info("=" * 60)
            else:
                Logger.error("AudioManager: Failed to load battle_music!")
        else:
            Logger.warning("AudioManager: No battle_music file registered")

    def stop_all_music(self):
        """Stop all background music playback."""
        if self.current_music and self.current_music.state == 'play':
            self.current_music.stop()
            Logger.info("AudioManager: All music stopped")