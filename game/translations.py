"""Multi-language translation system."""

from game.translation_strings import Translations


class LanguageManager:
    """Manages game language settings."""
    
    def __init__(self):
        """Initialize language manager."""
        self.current_language = 'zh'  # Default: Chinese
        self.translations = Translations()
    
    def set_language(self, lang_code):
        """
        Set the current language.
        
        Args:
            lang_code: 'zh' for Chinese, 'en' for English
        """
        if lang_code in ['zh', 'en']:
            self.current_language = lang_code
            print(f"[Language] Language set to: {lang_code}")
        else:
            print(f"[Language] Invalid language code: {lang_code}")
    
    def get(self, translation_key, *args):
        """
        Get translated text.
        
        Args:
            translation_key: Key from Translations class
            *args: Arguments to format into the string
            
        Returns:
            str: Translated and formatted text
        """
        # Get the translation dictionary
        translations_dict = getattr(self.translations, translation_key)
        
        # Get the text for current language
        text = translations_dict.get(self.current_language, translations_dict['en'])
        
        # Format with arguments if provided
        if args:
            try:
                return text.format(*args)
            except (IndexError, KeyError):
                return text
        
        return text
    
    def t(self, translation_key, *args):
        """
        Short alias for get().
        
        Args:
            translation_key: Key from Translations class
            *args: Arguments to format into the string
            
        Returns:
            str: Translated and formatted text
        """
        return self.get(translation_key, *args)


# Global language manager instance
language_manager = LanguageManager()


def get_text(translation_key, *args):
    """
    Get translated text using global language manager.
    
    Args:
        translation_key: Key from Translations class
        *args: Arguments to format into the string
        
    Returns:
        str: Translated and formatted text
    """
    return language_manager.get(translation_key, *args)


def t(translation_key, *args):
    """
    Short alias for get_text().
    
    Args:
        translation_key: Key from Translations class
        *args: Arguments to format into the string
        
    Returns:
        str: Translated and formatted text
    """
    return get_text(translation_key, *args)