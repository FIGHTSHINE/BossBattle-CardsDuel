"""Game mode selection section builder for main menu."""

from kivy.uix.label import Label
from kivy.uix.button import Button
from game.translations import t
from .menu_theme import MenuTheme


class ModeSectionBuilder:
    """Builder for game mode selection section."""
    
    @staticmethod
    def build(font_name, on_mode_selected):
        """
        Build game mode selection section.
        
        Args:
            font_name: Font name to use
            on_mode_selected: Callback when mode selected (receives mode string)
        
        Returns:
            List of widgets [mode_label, boss_duel_btn, survival_btn, pvp_btn]
        """
        widgets = []
        
        # Game mode selection label
        mode_label = Label(
            text=t('MENU_SELECT_MODE'),
            font_size=MenuTheme.FONT_SIZE_MODE_LABEL,
            size_hint_y=MenuTheme.SIZE_HINT_MODE_LABEL,
            color=MenuTheme.COLOR_MODE_LABEL,
            bold=True,
            font_name=font_name or 'Roboto'
        )
        widgets.append(mode_label)
        
        # Boss Duel button (working mode - green)
        boss_duel_btn = Button(
            text=t('MENU_MODE_BOSS_DUEL'),
            font_size=MenuTheme.FONT_SIZE_BOSS_DUEL,
            size_hint_y=MenuTheme.SIZE_HINT_BOSS_DUEL,
            bold=True,
            background_color=MenuTheme.COLOR_BOSS_DUEL,
            font_name=font_name or 'Roboto'
        )
        boss_duel_btn.bind(on_press=lambda instance: on_mode_selected('boss_duel'))
        widgets.append(boss_duel_btn)
        
        # Survival Mode (coming soon - grayed out)
        survival_btn = Button(
            text=t('MENU_MODE_SURVIVAL'),
            font_size=MenuTheme.FONT_SIZE_OTHER_MODES,
            size_hint_y=MenuTheme.SIZE_HINT_OTHER_MODES,
            background_color=MenuTheme.COLOR_SURVIVAL,
            font_name=font_name or 'Roboto',
            disabled=True
        )
        widgets.append(survival_btn)
        
        # PvP Mode (coming soon - grayed out)
        pvp_btn = Button(
            text=t('MENU_MODE_PVP'),
            font_size=MenuTheme.FONT_SIZE_OTHER_MODES,
            size_hint_y=MenuTheme.SIZE_HINT_OTHER_MODES,
            background_color=MenuTheme.COLOR_PVP,
            font_name=font_name or 'Roboto',
            disabled=True
        )
        widgets.append(pvp_btn)
        
        return widgets