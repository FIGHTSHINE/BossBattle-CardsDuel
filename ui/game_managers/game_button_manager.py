"""Game button management and creation."""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from ui.font_config import get_chinese_font_name
from game.translations import Translations as T
from utils.screen_config import ScreenConfig
from kivy.core.window import Window

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

        Uses absolute positioning and ensures buttons are on top layer.

        Args:
            restart_text: Text for restart button
            on_restart: Callback for restart button
            on_menu: Callback for menu button
        """
        # ✅ 计算按钮尺寸
        button_width = ScreenConfig.scale_width(400)
        button_height = ScreenConfig.scale_height(60)

        # ✅ 计算按钮位置（屏幕底部，从底部算起 15% 高度）
        button_x = (Window.width - button_width) / 2
        button_y = Window.height * 0.15  # ← 改为 0.15（底部）

        # ✅ 创建按钮布局
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(button_width, button_height),
            pos=(button_x, button_y),
            spacing=ScreenConfig.scale_spacing(10)
        )

        # Create and add restart button
        restart_btn = self._create_restart_button(restart_text, on_restart)
        button_layout.add_widget(restart_btn)

        # Create and add menu button
        menu_btn = self._create_menu_button(on_menu)
        button_layout.add_widget(menu_btn)

        # ✅ 添加到 effects_overlay
        if hasattr(self.parent, 'effects_overlay'):
            # ✅ 确保按钮在最顶层（使用 index=0）
            self.parent.effects_overlay.add_widget(button_layout, index=0)
            print(f"[GameButtonManager] Added buttons at pos=({button_x:.1f}, {button_y:.1f}), index=0 (top layer)")
        else:
            # Fallback
            print(f"[GameButtonManager] WARNING: effects_overlay not found, using parent")
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
            font_size=ScreenConfig.scale_font_size(20),
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
            font_size=ScreenConfig.scale_font_size(20),
            bold=True,
            background_color=(0.8, 0.6, 0.2, 1),  # Orange/yellow
            font_name=self.chinese_font
        )
        btn.bind(on_press=callback)
        return btn