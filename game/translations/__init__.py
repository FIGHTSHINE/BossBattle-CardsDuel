"""Translation system for multi-language support."""

from .translations import LanguageManager
from .translations import language_manager  # ✅ 导入全局实例
from .translation_strings import Translations
from .ui_translations import UITranslations
from .message_translations import MessageTranslations
from .menu_translations import MenuTranslations
from .log_translations import LogTranslations

# ✅ 添加 t() 函数别名
def t(key, *args):
    """
    Convenience function for translation.
    
    Args:
        key: Translation key
        *args: Arguments to format into the string
    
    Returns:
        str: Translated text
    """
    return language_manager.get(key, *args)

__all__ = [
    'LanguageManager',
    'Translations',
    'UITranslations',
    'MessageTranslations',
    'MenuTranslations',
    'LogTranslations',
    'language_manager',
    't',  # ✅ 添加到导出列表
]