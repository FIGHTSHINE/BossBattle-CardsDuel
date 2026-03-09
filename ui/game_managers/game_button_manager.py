"""Game button management and creation."""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from ui.font_config import get_chinese_font_name
from game.translations import Translations as T


class GameButtonManager:
    """Manages game-over and action buttons."""
    
    def __init__(self, parent_layout):
        """
        Initialize button manager.
        
        Args:
            parent_layout: Parent layout to add buttons to
        """
        self.parent = parent_layout
        self.chinese_font = get_chinese_font_name()
    
    def add_game_over_buttons(self, restart_text, on_restart, on_menu):
        """
        Add restart and menu buttons to screen.
        
        Args:
            restart_text: Text for restart button
            on_restart: Callback for restart button
            on_menu: Callback for menu button
        """
        # Create horizontal layout for buttons
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1,
            spacing='10sp'
        )
        
        # Create and add restart button
        restart_btn = self._create_restart_button(restart_text, on_restart)
        button_layout.add_widget(restart_btn)
        
        # Create and add menu button
        menu_btn = self._create_menu_button(on_menu)
        button_layout.add_widget(menu_btn)
        
        # Add button layout to parent
        self.parent.add_widget(button_layout)
    
    def _create_restart_button(self, text, callback):
        """
        Create restart button.
        
        Args:
            text: Button text
            callback: Button press callback
            
        Returns:
            Button widget
        """
        btn = Button(
            text=text,
            font_size='20sp',
            bold=True,
            background_color=(0.2, 0.6, 1, 1),
            font_name=self.chinese_font
        )
        btn.bind(on_press=callback)
        return btn
    
    def _create_menu_button(self, callback):
        """
        Create return to menu button.
        
        Args:
            callback: Button press callback
            
        Returns:
            Button widget
        """
        btn = Button(
            text=T.MENU_BACK_TO_MAIN['zh'],
            font_size='20sp',
            bold=True,
            background_color=(0.8, 0.6, 0.2, 1),  # Orange/yellow
            font_name=self.chinese_font
        )
        btn.bind(on_press=callback)
        return btn