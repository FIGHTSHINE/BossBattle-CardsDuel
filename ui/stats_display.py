"""Stats display component."""

from typing import Optional
from game.translation_strings import Translations as T
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from game.translations import language_manager
from ui.ui_logger import UILogger
from ui.ui_builder import UIBuilder


class StatsDisplay(BoxLayout):
    """Displays game statistics (HP, shield, turn, etc)."""
    
    def __init__(self, **kwargs):
        """Initialize stats display."""
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = 0.5
        self.spacing = '5sp'
        self.builder: Optional[UIBuilder] = None
        self.logger = UILogger()
        self.labels = {}
        self.boss_widget = None  # Boss widget reference
        self.boss_health_bar = None
        self.player_widget = None
        self.player_health_bar = None
        self._initialized = False  # ✅ 添加初始化标志
    
    def build_stats(self, builder):
        """
        Build all stats labels.
        
        Args:
            builder: UIBuilder instance
        """
        self.builder = builder  # Save builder for later use
        # Turn counter
        self.labels['turn'] = builder.build_turn_counter(1)
        self.add_widget(self.labels['turn'])
        
        # Turn indicator
        self.labels['turn_indicator'] = builder.build_turn_indicator()
        self.add_widget(self.labels['turn_indicator'])
        
        # Boss HP - WITH VISUAL WIDGET AND HEALTH BAR
        boss_layout, self.boss_widget, boss_hp_label, self.boss_health_bar = builder.build_boss_widget(300, 300)
        self.add_widget(boss_layout)
        self.labels['boss_hp'] = boss_hp_label  # Store label for text updates

        # ⚠️ ADD: Boss special attack warning label (initially hidden)
        self.labels['boss_warning'] = self._build_boss_warning_label()
        self.add_widget(self.labels['boss_warning'])
        
        # Battle area
        self.labels['battle_area'] = builder.build_battle_area()
        self.add_widget(self.labels['battle_area'])
        
        # Player HP
        player_layout, self.player_widget, player_hp_label, self.player_health_bar = builder.build_player_widget(100, 100, 0)
        self.add_widget(player_layout)
        self.labels['player_hp'] = player_hp_label  # Store label for text updates
        
        # Shield
        self.labels['shield'] = builder.build_shield_label()
        self.add_widget(self.labels['shield'])
        
        # Cards info
        self.labels['cards'] = builder.build_cards_label()
        self.add_widget(self.labels['cards'])
        
        # Cards played this turn
        self.labels['cards_played'] = builder.build_cards_played_label()
        self.add_widget(self.labels['cards_played'])
    
    def add_end_turn_button(self, callback):
        """
        Add end turn button.
        
        Args:
            callback: Function to call when button is pressed
        """
        btn = self.builder.build_end_turn_button(callback) #type: ignore
        self.add_widget(btn)
        self.labels['end_turn'] = btn
    
    def update_stats(self, stats):
        """
        Update all stats labels.
        
        Args:
            stats: Dictionary with game stats
        """
        # ✅ 修改：使用翻译系统
        self.labels['turn'].text = T.UI_TURN_COUNTER['zh'].format(stats['turn'])
        
        # Update boss HP text, widget visual state, and health bar
        self.labels['boss_hp'].text = f"👹 BOSS: {stats['boss_hp']}/{stats['boss_max_hp']}"
        
        if self.boss_widget:
            hp_percent = (stats['boss_hp'] / stats['boss_max_hp']) * 100
            self.boss_widget.hp_percent = hp_percent
        
        if self.boss_health_bar:
            self.boss_health_bar.update_hp(stats['boss_hp'], stats['boss_max_hp'])
        
        # ⚠️ ADD: Show boss warning if HP is low (≤40%)
        boss_hp_percent = (stats['boss_hp'] / stats['boss_max_hp']) * 100
        if boss_hp_percent <= 40:
            self.labels['boss_warning'].opacity = 1
            # ✅ 修改：使用翻译系统
            self.labels['boss_warning'].text = T.UI_BOSS_WARNING['zh']
        else:
            self.labels['boss_warning'].opacity = 0

        # ✅ 添加以下代码：更新 player widget
        if self.player_widget:
            player_hp_percent = (stats['player_hp'] / stats['player_max_hp']) * 100
            self.player_widget.hp_percent = player_hp_percent
            self.player_widget.shield = stats['shield']
        
        if self.player_health_bar:
            self.player_health_bar.update_hp(stats['player_hp'], stats['player_max_hp'])
        
        self.labels['player_hp'].text = f"❤️ YOU: {stats['player_hp']}/{stats['player_max_hp']}"
        # ✅ 添加这一行：更新护盾标签
        self.labels['shield'].text = f"🛡️ 护盾: {stats['shield']}"
        
        # Update cards info
        hand = stats['cards_in_hand']
        deck = stats['cards_in_deck']
        used = stats['cards_used']
        
        # ✅ 修改：使用翻译系统
        if deck == 0:
            self.labels['cards'].text = T.UI_CARDS_DECK_EMPTY['zh'].format(hand, used)
            self.labels['cards'].color = (1, 0.5, 0, 1)
        else:
            self.labels['cards'].text = T.UI_CARDS_REMAINING['zh'].format(hand, deck, used)
            self.labels['cards'].color = (0.8, 0.8, 0.8, 1)
    
    def update_turn_indicator(self, is_player_turn):
        """
        Update turn indicator.
        
        Args:
            is_player_turn: Boolean indicating if it's player's turn
        """
        # ✅ 修改：使用翻译系统
        if is_player_turn:
            self.labels['turn_indicator'].text = T.UI_TURN_PLAYER['zh']
            self.labels['turn_indicator'].color = (0.3, 1, 0.5, 1)
        else:
            self.labels['turn_indicator'].text = T.UI_TURN_BOSS['zh']
            self.labels['turn_indicator'].color = (1, 0.3, 0.3, 1)
    
    def update_battle_area(self, text, color=(0.9, 0.9, 0.9, 1)):
        """
        Update battle area text and color.
        
        Args:
            text: Text to display
            color: RGB color tuple
        """
        self.labels['battle_area'].text = text
        self.labels['battle_area'].color = color
    
    def update_cards_played(self, current, max_cards):
        """
        Update cards played counter.
        
        Args:
            current: Current cards played
            max_cards: Maximum cards allowed
        """
        # ✅ 修改：使用翻译系统
        self.labels['cards_played'].text = T.UI_CARDS_THIS_TURN['zh'].format(current, max_cards)
    
    def set_low_hp_warning(self):
        """Set player HP to warning color."""
        self.labels['player_hp'].color = (1, 0.3, 0.3, 1)
    
    def set_normal_hp_color(self):
        """Set player HP to normal color."""
        self.labels['player_hp'].color = (0.3, 1, 0.3, 1)
    
    def show_win(self, turns):
        """
        Show victory screen.
        
        Args:
            turns: Number of turns taken
        """
        self.labels['boss_hp'].color = (0, 1, 0, 1)
        # ✅ 修改：使用翻译系统
        victory_text = f"[size=28][color=00ff00]🎉 胜利! 🎉[/color][/size]\n[size=20]{T.UI_VICTORY_TURNS['zh'].format(turns)}[/size]"
        self.labels['battle_area'].text = victory_text
        self.labels['battle_area'].color = (0, 1, 0, 1)
    
    def show_lose(self, turns):
        """
        Show defeat screen.
        
        Args:
            turns: Number of turns survived
        """
        self.labels['player_hp'].color = (1, 0, 0, 1)
        # ✅ 修改：使用翻译系统
        defeat_text = f"[size=28][color=ff3333]💀 失败 💀[/color][/size]\n[size=20]{T.UI_DEFEAT_TURNS['zh'].format(turns)}[/size]"
        self.labels['battle_area'].text = defeat_text
        self.labels['battle_area'].color = (1, 0.2, 0.2, 1)
        
        
    def _build_boss_warning_label(self):
        """
        Build boss special attack warning label.
        
        Returns:
            Label: Configured warning label (initially hidden)
        """
        warning_label = Label(
            # ✅ fix
            text=T.UI_BOSS_WARNING.get(language_manager.current_language, T.UI_BOSS_WARNING['en']),
            size_hint_y=None,
            height='40sp',  # 保持初始高度
            color=(1, 0.3, 0, 1),  # Orange-red color
            bold=True,
            halign='center',
            valign='middle',
            font_size='18sp',
            opacity=0,  # Initially hidden
            markup=True,
            text_size=(None, None),  # ✅ 添加：让文本自动换行
            size_hint_x=1  # ✅ 添加：宽度自适应
        )
        
        # ✅ 添加：根据文本内容自动调整高度
        warning_label.bind(texture_size=warning_label.setter('size'))
        
        return warning_label
    
    def hide_boss_special_attack_warning(self):
        """
        Hide the boss special attack warning.
        
        Called after boss has used the special attack.
        """
        if 'boss_warning' in self.labels:
            self.labels['boss_warning'].opacity = 0
            print(f"[UI] Boss special attack warning hidden")
    
    def show_boss_special_attack_used(self):
        """
        Show message that boss has used special attack.
        
        Displays in battle area for one turn.
        """
        if 'battle_area' in self.labels:
            # ✅ 修改：汉化 Boss 大招使用提示
            self.labels['battle_area'].text = "[size=20][color=ff6600]🔥 Boss 已使用大招! 🔥[/color][/size]"
            self.labels['battle_area'].color = (1, 0.4, 0, 1)