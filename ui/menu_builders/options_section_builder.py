"""Options section builder for main menu."""

from kivy.uix.label import Label
from kivy.uix.button import Button
from game.translations import t, language_manager
from .menu_theme import MenuTheme


class OptionsSectionBuilder:
    """Builder for options section (language, about, exit)."""
    
    @staticmethod
    def build(font_name, on_language, on_about, on_exit):
        """
        Build options section with language indicator and buttons.
        
        Args:
            font_name: Font name to use
            on_language: Callback for language button
            on_about: Callback for about button
            on_exit: Callback for exit button
        
        Returns:
            List of widgets [spacer, options_label, lang_btn, about_btn, exit_btn, lang_indicator]
        """
        widgets = []
        
        # Spacer
        spacer = Label(
            text='',
            size_hint_y=MenuTheme.SIZE_HINT_SPACER
        )
        widgets.append(spacer)
        
        # Options label
        options_label = Label(
            text=t('MENU_OPTIONS'),
            font_size=MenuTheme.FONT_SIZE_OPTIONS_LABEL,
            size_hint_y=MenuTheme.SIZE_HINT_OPTIONS_LABEL,
            color=MenuTheme.COLOR_OPTIONS_LABEL,
            font_name=font_name or 'Roboto'
        )
        widgets.append(options_label)
        
        # Language button (blue)
        lang_btn = Button(
            text=t('MENU_LANGUAGE'),
            font_size=MenuTheme.FONT_SIZE_OPTIONS_BTN,
            size_hint_y=MenuTheme.SIZE_HINT_OPTIONS_BTN,
            background_color=MenuTheme.COLOR_LANGUAGE,
            font_name=font_name or 'Roboto'
        )
        lang_btn.bind(on_press=lambda i: on_language())
        widgets.append(lang_btn)
        
        # About button (purple)
        about_btn = Button(
            text=t('MENU_ABOUT'),
            font_size=MenuTheme.FONT_SIZE_OPTIONS_BTN,
            size_hint_y=MenuTheme.SIZE_HINT_OPTIONS_BTN,
            background_color=MenuTheme.COLOR_ABOUT,
            font_name=font_name or 'Roboto'
        )
        about_btn.bind(on_press=lambda i: on_about())
        widgets.append(about_btn)
        
        # Exit button (red)
        exit_btn = Button(
            text=t('MENU_EXIT'),
            font_size=MenuTheme.FONT_SIZE_OPTIONS_BTN,
            size_hint_y=MenuTheme.SIZE_HINT_OPTIONS_BTN,
            background_color=MenuTheme.COLOR_EXIT,
            font_name=font_name or 'Roboto'
        )
        exit_btn.bind(on_press=lambda i: on_exit())
        widgets.append(exit_btn)
        
        # Language indicator
        lang_indicator = Label(
            text=f"Language: {language_manager.current_language.upper()} | 语言: {language_manager.current_language.upper()}",
            font_size=MenuTheme.FONT_SIZE_LANG_INDICATOR,
            size_hint_y=MenuTheme.SIZE_HINT_LANG_INDICATOR,
            color=MenuTheme.COLOR_LANG_INDICATOR,
            font_name=font_name or 'Roboto'
        )
        widgets.append(lang_indicator)
        
        return widgets