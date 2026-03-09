"""Platform-specific directory management for audio files."""

import os
from kivy.utils import platform
from kivy.logger import Logger


class PlatformManager:
    """Manages platform-specific temporary directories."""
    
    @staticmethod
    def get_platform():
        """Get current platform name."""
        return platform
    
    @staticmethod
    def get_temp_dir():
        """Get platform-specific temporary directory for audio files."""
        if platform == 'android':
            try:
                from android.storage import primary_external_storage_path  # type: ignore
                return os.path.join(primary_external_storage_path(), 'bossbattle_sounds')
            except ImportError:
                Logger.warning("PlatformManager: Android storage not available")
                return os.path.join(os.path.expanduser('~'), 'bossbattle_sounds')
        elif platform == 'win':
            temp = os.environ.get('TEMP', '.')
            return os.path.join(temp, 'bossbattle_sounds')
        else:
            return '/tmp/bossbattle_sounds'
    
    @staticmethod
    def ensure_temp_dir(temp_dir):
        """Ensure temp directory exists."""
        if not os.path.exists(temp_dir):
            try:
                os.makedirs(temp_dir)
                Logger.info(f"PlatformManager: Created {temp_dir}")
            except Exception as e:
                Logger.error(f"PlatformManager: Failed to create: {e}")