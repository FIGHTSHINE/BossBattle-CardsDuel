"""Title section builder for main menu."""

from kivy.uix.label import Label
from game.translations import t
from .menu_theme import MenuTheme


class TitleBuilder:
    """Builder for main menu title section."""
    
    @staticmethod
    def build(font_name):
        """
        Build title label widget.
        
        Args:
            font_name: Font name to use
        
        Returns:
            Label widget configured as title
        """
        title = Label(
            text=t('MENU_TITLE'),
            font_size=MenuTheme.FONT_SIZE_TITLE,
            size_hint_y=MenuTheme.SIZE_HINT_TITLE,
            color=MenuTheme.COLOR_TITLE,
            bold=True,
            font_name=font_name or 'Roboto',
            halign=MenuTheme.TITLE_HALIGN,
            valign=MenuTheme.TITLE_VALIGN
        )
        return title