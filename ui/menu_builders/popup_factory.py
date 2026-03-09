"""Popup factory for main menu."""

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.logger import Logger

from game.translations import t, language_manager
from .menu_theme import MenuTheme


class PopupFactory:
    """Factory for creating standardized popups."""
    
    @staticmethod
    def create_rules_popup(mode, font_name, on_confirm):
        """
        Create game mode rules confirmation popup.
        
        Args:
            mode: Game mode string ('boss_duel', 'survival', 'pvp')
            font_name: Font name for text
            on_confirm: Callback when confirm button pressed (receives no args)
        
        Returns:
            Popup instance ready to open
        """
        try:
            print(f"[PopupFactory] Creating rules popup for mode: {mode}")
            
            # Get rules text based on mode
            rules_key = f'MODE_RULES_{mode.upper()}'
            rules_text = t(rules_key)
            
            # Create popup content layout
            rules_content = BoxLayout(
                orientation='vertical',
                padding=MenuTheme.POPUP_PADDING,
                spacing=MenuTheme.POPUP_SPACING
            )
            
            # Add semi-transparent background with rounded corners
            with rules_content.canvas.before:
                Color(*MenuTheme.COLOR_POPUP_BG)
                rules_content._popup_bg = RoundedRectangle(
                    size=rules_content.size,
                    pos=rules_content.pos,
                    radius=MenuTheme.POPUP_BORDER_RADIUS
                )
            
            # Update background when size/position changes
            rules_content.bind(size=PopupFactory._update_popup_bg, pos=PopupFactory._update_popup_bg)
            
            # Title label
            title_label = Label(
                text=t('POPUP_TITLE_RULES'),
                font_size=MenuTheme.FONT_SIZE_POPUP_TITLE,
                size_hint_y=MenuTheme.SIZE_HINT_RULES_TITLE,
                bold=True,
                color=MenuTheme.COLOR_RULES_TITLE,
                font_name=font_name or 'Roboto',
                halign=MenuTheme.TITLE_HALIGN,
                valign=MenuTheme.TITLE_VALIGN
            )
            rules_content.add_widget(title_label)
            
            # Rules text label
            rules_label = Label(
                text=rules_text,
                font_size=MenuTheme.FONT_SIZE_RULES_TEXT,
                size_hint_y=MenuTheme.SIZE_HINT_RULES_TEXT,
                font_name=font_name or 'Roboto',
                halign=MenuTheme.RULES_TEXT_HALIGN,
                valign=MenuTheme.RULES_TEXT_VALIGN,
                text_size=(Window.width * MenuTheme.RULES_TEXT_WIDTH_RATIO, None),
                markup=True,
                color=MenuTheme.COLOR_RULES_TEXT
            )
            rules_content.add_widget(rules_label)
            
            # Button layout (horizontal)
            button_layout = BoxLayout(
                orientation='horizontal',
                spacing=MenuTheme.POPUP_BUTTON_SPACING,
                size_hint_y=MenuTheme.SIZE_HINT_RULES_BUTTONS
            )
            
            # Back button
            back_btn = Button(
                text=t('POPUP_BACK'),
                font_size=MenuTheme.FONT_SIZE_POPUP_BTN,
                background_color=MenuTheme.COLOR_POPUP_BACK_BTN,
                font_name=font_name or 'Roboto',
                color=(1, 1, 1, 1)
            )
            
            # Confirm button
            confirm_btn = Button(
                text=t('POPUP_CONFIRM'),
                font_size=MenuTheme.FONT_SIZE_POPUP_BTN,
                background_color=MenuTheme.COLOR_POPUP_CONFIRM_BTN,
                font_name=font_name or 'Roboto',
                color=(1, 1, 1, 1)
            )
            
            button_layout.add_widget(back_btn)
            button_layout.add_widget(confirm_btn)
            rules_content.add_widget(button_layout)
            
            # Create popup
            popup = Popup(
                title='',  # Empty - we use custom title label
                content=rules_content,
                size_hint=MenuTheme.POPUP_RULES_SIZE,
                auto_dismiss=False,
                background_color=MenuTheme.COLOR_POPUP_OVERLAY,
                separator_height=0
            )
            
            # Bind buttons
            back_btn.bind(on_press=lambda instance: popup.dismiss())
            confirm_btn.bind(on_press=lambda instance: on_confirm())
            
            Logger.info(f"PopupFactory: Created rules popup for mode '{mode}'")
            return popup
            
        except Exception as e:
            Logger.error(f"PopupFactory: Failed to create rules popup: {e}")
            raise
    
    @staticmethod
    def create_about_popup(font_name):
        """
        Create about popup dialog.
        
        Args:
            font_name: Font name for text
        
        Returns:
            Popup instance ready to open
        """
        try:
            print("[PopupFactory] Creating about popup")
            
            # Create content layout
            about_content = BoxLayout(
                orientation='vertical',
                padding=MenuTheme.PADDING,
                spacing=MenuTheme.SPACING
            )
            
            # Title label
            title_label = Label(
                text=t('MENU_ABOUT_TITLE'),
                font_size=MenuTheme.FONT_SIZE_ABOUT_TITLE,
                bold=True,
                font_name=font_name or 'Roboto'
            )
            
            # Content label
            content_label = Label(
                text=t('MENU_ABOUT_CONTENT'),
                font_size=MenuTheme.FONT_SIZE_ABOUT_CONTENT,
                size_hint_y=MenuTheme.SIZE_HINT_ABOUT_CONTENT,
                font_name=font_name or 'Roboto',
                halign=MenuTheme.ABOUT_CONTENT_HALIGN,
                valign=MenuTheme.ABOUT_CONTENT_VALIGN,
                text_size=(Window.width * MenuTheme.ABOUT_CONTENT_WIDTH_RATIO, None)
            )
            
            # Close button
            close_btn = Button(
                text='OK',
                font_size=MenuTheme.FONT_SIZE_ABOUT_BTN,
                size_hint_y=MenuTheme.SIZE_HINT_ABOUT_BTN,
                background_color=(0.5, 0.5, 0.5, 1),
                font_name=font_name or 'Roboto'
            )
            
            about_content.add_widget(title_label)
            about_content.add_widget(content_label)
            about_content.add_widget(close_btn)
            
            # Create popup
            popup = Popup(
                title='About',
                content=about_content,
                size_hint=MenuTheme.POPUP_ABOUT_SIZE,
                auto_dismiss=False
            )
            
            # Bind close button
            close_btn.bind(on_press=lambda instance: popup.dismiss())
            
            Logger.info("PopupFactory: Created about popup")
            return popup
            
        except Exception as e:
            Logger.error(f"PopupFactory: Failed to create about popup: {e}")
            raise
    
    @staticmethod
    def _update_popup_bg(instance, value):
        """
        Update popup background size and position.
        
        Args:
            instance: The layout instance
            value: New size/position value
        """
        if hasattr(instance, '_popup_bg'):
            instance._popup_bg.size = instance.size
            instance._popup_bg.pos = instance.pos