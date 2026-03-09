"""UI component builder for game screen."""

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from ui.player.player_widget import PlayerWidget
from ui.player.player_health_bar import PlayerHealthBar
from ui.ui_logger import UILogger
from ui.font_config import get_chinese_font_name
from game.translations import t
from ui.boss.boss_widget import BossWidget
from ui.boss.boss_health_bar import BossHealthBar

class UIBuilder:
    """Builds UI components for the game screen."""
    
    def __init__(self, parent_layout):
        """
        Initialize UI builder.
        
        Args:
            parent_layout: The parent GameScreen instance
        """
        self.parent = parent_layout
        self.logger = UILogger()
        self.chinese_font = get_chinese_font_name()
        
        # ✅ 运行时保护
        if self.chinese_font is None:
            print("[UIBuilder] ❌ CRITICAL: Font is None, forcing to 'Roboto'")
            self.chinese_font = 'Roboto'
        
        print(f"[UIBuilder] ✅ Using font: '{self.chinese_font}'")
    
    def build_turn_counter(self, turn):
        """Build turn counter label."""
        label = Label(
            text=t('UI_TURN_COUNTER', turn),
            font_size='20sp',
            size_hint_y=0.05,
            color=(0.8, 0.8, 0.8, 1),
            font_name=self.chinese_font or 'Roboto'
        )
        self.logger.log_ui_component_added("Turn counter")
        return label
    
    def build_turn_indicator(self):
        """Build turn indicator label."""
        label = Label(
            text=t('UI_TURN_PLAYER'),
            font_size='24sp',
            size_hint_y=0.08,
            color=(0.3, 1, 0.5, 1),  # Green for player turn
            bold=True,
            font_name=self.chinese_font or 'Roboto'
        )
        self.logger.log_ui_component_added("Turn indicator")
        return label
    
    def build_boss_label(self, boss_hp, boss_max_hp):
        """Build boss HP label."""
        label = Label(
            text=t('UI_BOSS_HP', boss_hp, boss_max_hp),
            font_size='32sp',
            size_hint_y=0.09,
            color=(1, 0.3, 0.3, 1),
            bold=True,
            font_name=self.chinese_font or 'Roboto'
        )
        self.logger.log_ui_component_added("Boss HP label")
        return label
    
    def build_boss_widget(self, boss_hp=300, boss_max_hp=300):
        """
        Build boss visual widget with HP label and health bar.
        
        Args:
            boss_hp: Current boss HP
            boss_max_hp: Maximum boss HP
            
        Returns:
            tuple: (boss_layout, boss_widget, hp_label, health_bar)
        """
        # Create vertical layout for boss + health bar
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.2,
            spacing='5sp'
        )
        
        # Boss visual + HP text (horizontal)
        boss_visual_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.5,
            spacing='10sp',
            padding='5sp'
        )
        
        # Boss visual widget
        boss_widget = BossWidget()
        boss_widget.hp_percent = (boss_hp / boss_max_hp) * 100
        boss_visual_layout.add_widget(boss_widget)
        
        # Boss HP text label (larger, above health bar)
        hp_label = Label(
            text=t('UI_BOSS_HP', boss_hp, boss_max_hp),
            font_size='24sp',
            size_hint_x=0.7,
            color=(1, 0.3, 0.3, 1),
            bold=True,
            font_name=self.chinese_font or 'Roboto',
            halign='left',
            valign='middle'
        )
        boss_visual_layout.add_widget(hp_label)
        
        main_layout.add_widget(boss_visual_layout)
        
        # Dynamic health bar (below boss visual)
        health_bar = BossHealthBar()
        health_bar.update_hp(boss_hp, boss_max_hp)
        main_layout.add_widget(health_bar)
        
        self.logger.log_ui_component_added("Boss widget with health bar")
        return main_layout, boss_widget, hp_label, health_bar
    
    def build_player_widget(self, player_hp=200, player_max_hp=200, player_shield=0):
        """
        Build player visual widget with HP label and health bar.
        
        Args:
            player_hp: Current player HP
            player_max_hp: Maximum player HP
            player_shield: Current player shield value
            
        Returns:
            tuple: (player_layout, player_widget, hp_label, health_bar)
        """
        
        # Create vertical layout for player + health bar
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.25,
            spacing='5sp'
        )
        
        # Player visual + HP text (horizontal)
        player_visual_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.5,
            spacing='10sp',
            padding='5sp'
        )
        
        # Player HP text label (left side)
        hp_label = Label(
            text=t('UI_PLAYER_HP', player_hp, player_max_hp),
            font_size='20sp',
            size_hint_x=0.7,
            color=(0.3, 1, 0.5, 1),  # Green for player
            bold=True,
            font_name=self.chinese_font or 'Roboto',
            halign='left',
            valign='middle'
        )
        player_visual_layout.add_widget(hp_label)
        
        # Player visual widget (right side)
        player_widget = PlayerWidget()
        player_widget.hp_percent = (player_hp / player_max_hp) * 100
        player_widget.shield = player_shield
        player_visual_layout.add_widget(player_widget)
        
        main_layout.add_widget(player_visual_layout)
        
        # Dynamic health bar (below player visual)
        health_bar = PlayerHealthBar()
        health_bar.update_hp(player_hp, player_max_hp)
        main_layout.add_widget(health_bar)
        
        self.logger.log_ui_component_added("Player widget with health bar")
        return main_layout, player_widget, hp_label, health_bar

    def build_battle_area(self):
        """Build battle area label."""
        label = Label(
            text=t('UI_BATTLE_AREA_START'),
            font_size='20sp',
            size_hint_y=0.18,
            color=(0.9, 0.9, 0.9, 1),
            halign='center',
            valign='middle',
            markup=True,
            font_name=self.chinese_font or 'Roboto'
        )
        self.logger.log_ui_component_added("Battle area")
        return label
    
    def build_player_label(self, player_hp, player_max_hp):
        """Build player HP label."""
        label = Label(
            text=t('UI_PLAYER_HP', player_hp, player_max_hp),
            font_size='24sp',
            size_hint_y=0.07,
            color=(0.3, 1, 0.3, 1),
            bold=True,
            font_name=self.chinese_font or 'Roboto'
        )
        self.logger.log_ui_component_added("Player HP label")
        return label
    
    def build_shield_label(self, shield_value=0):
        """Build shield indicator label."""
        label = Label(
            text=t('UI_SHIELD_UP', shield_value),
            font_size='18sp',
            size_hint_y=0.04,
            color=(0.3, 0.6, 1, 1),
            font_name=self.chinese_font or 'Roboto'
        )
        self.logger.log_ui_component_added("Shield label")
        return label
    
    def build_cards_label(self):
        """Build cards remaining label."""
        label = Label(
            text=t('UI_CARDS_REMAINING', 20),
            font_size='18sp',
            size_hint_y=0.04,
            color=(0.8, 0.8, 0.8, 1),
            font_name=self.chinese_font or 'Roboto'
        )
        self.logger.log_ui_component_added("Cards remaining label")
        return label
    
    def build_cards_played_label(self):
        """Build cards played counter label."""
        label = Label(
            text=t('UI_CARDS_THIS_TURN', 0, 3),
            font_size='16sp',
            size_hint_y=0.04,
            color=(0.7, 0.7, 0.7, 1),
            font_name=self.chinese_font or 'Roboto'
        )
        self.logger.log_ui_component_added("Cards played counter")
        return label
    
    def build_end_turn_button(self, callback):
        """
        Build end turn button.
        
        Args:
            callback: Function to call when button is pressed
        """
        button = Button(
            text= t('UI_END_TURN'),
            size_hint_y=0.08,
            font_size='20sp',
            bold=True,
            background_color=(0.8, 0.4, 0.2, 1),  # Orange
            font_name=self.chinese_font or 'Roboto'
        )
        button.bind(on_press=callback)
        self.logger.log_ui_component_added("End turn button")
        return button
    
    def build_card_scroll(self):
        """Build card scroll area."""
        scroll = ScrollView(
            size_hint_y=0.39,
            bar_width='10sp'
        )
        
        layout = BoxLayout(
            size_hint_y=None,
            spacing='8sp',
            padding='10sp'
        )
        layout.bind(minimum_height=layout.setter('height'))
        
        scroll.add_widget(layout)
        self.logger.log_ui_component_added("Card scroll area")
        
        return scroll, layout
    
    def build_card_button(self, card, callback):
        """
        Build a single card button.
        
        Args:
            card: Card object
            callback: Function to call when button is pressed
        """
        card_icons = {
            "attack": "⚔️",
            "heal": "💚",
            "shield": "🛡️",
            "critical": "💥"
        }
        
        icon = card_icons.get(card.card_type.value, "❓")
        
        btn = Button(
            text=f"{icon}\n{card.name}\n{card.value}",
            size_hint=(None, None),
            size=(140, 100),
            font_size='14sp',  # Slightly smaller for Chinese text
            bold=True,
            font_name=self.chinese_font or 'Roboto'
        )
        btn.background_color = card.color
        
        # Add border effect for critical cards
        if card.card_type.value == "critical":
            btn.border_width = 3
        
        # Store card reference and bind callback
        btn.card_id = card.unique_id
        btn.bind(on_press=lambda instance, c=card: callback(c))
        
        return btn
    
    def build_restart_button(self, button_text, callback):
        """
        Build restart button.
        
        Args:
            button_text: Text to display on button
            callback: Function to call when button is pressed
        """
        button = Button(
            text=button_text,
            size_hint_y=0.1,
            font_size='22sp',
            bold=True,
            background_color=(0.2, 0.6, 1, 1),
            font_name=self.chinese_font or 'Roboto'
        )
        button.bind(on_press=callback)
        return button