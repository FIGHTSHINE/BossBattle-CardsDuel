from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from dataclasses import dataclass

# ========== DATA CLASSES ==========
@dataclass
class Card:
    name: str
    damage: int

# ========== GAME LOGIC ==========
class BattleManager:
    def __init__(self):
        self.boss_max_hp = 250
        self.player_max_hp = 80
        self.boss_hp = self.boss_max_hp
        self.player_hp = self.player_max_hp
        self.boss_damage = 5
    
    def play_card(self, damage):
        self.boss_hp -= damage
        self.player_hp -= self.boss_damage
        
        if self.boss_hp <= 0:
            return "win"
        elif self.player_hp <= 0:
            return "lose"
        return "playing"
    
    def reset(self):
        self.boss_hp = self.boss_max_hp
        self.player_hp = self.player_max_hp

# ========== UI COMPONENTS ==========
class GameScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = '20sp'
        self.spacing = '10sp'
        
        # Game state
        self.battle = BattleManager()
        self.cards = []
        self.game_over = False
        
        # Build UI
        self.build_ui()
    
    def build_ui(self):
        # Boss HP (top)
        self.boss_label = Label(
            text=f"👹 BOSS: {self.battle.boss_hp}/{self.battle.boss_max_hp}",
            font_size='36sp',
            size_hint_y=0.12,
            color=(1, 0.3, 0.3, 1),
            bold=True
        )
        self.add_widget(self.boss_label)
        
        # Battle area (center)
        self.battle_area = Label(
            text="Choose a card to attack!",
            font_size='22sp',
            size_hint_y=0.25,
            color=(0.9, 0.9, 0.9, 1)
        )
        self.add_widget(self.battle_area)
        
        # Player HP
        self.player_label = Label(
            text=f"❤️ YOU: {self.battle.player_hp}/{self.battle.player_max_hp}",
            font_size='28sp',
            size_hint_y=0.08,
            color=(0.3, 1, 0.3, 1),
            bold=True
        )
        self.add_widget(self.player_label)
        
        # Cards remaining counter
        self.cards_label = Label(
            text=f"Cards: 15",
            font_size='20sp',
            size_hint_y=0.05,
            color=(0.8, 0.8, 0.8, 1)
        )
        self.add_widget(self.cards_label)
        
        # Card hand (scrollable)
        self.card_scroll = ScrollView(
            size_hint_y=0.5,
            bar_width='10sp'
        )
        self.card_layout = BoxLayout(
            size_hint_y=None,
            spacing='8sp',
            padding='10sp'
        )
        self.card_layout.bind(minimum_height=self.card_layout.setter('height'))
        self.card_scroll.add_widget(self.card_layout)
        self.add_widget(self.card_scroll)
        
        # Create and display cards
        self.create_cards()
        self.create_card_buttons()
    
    def create_cards(self):
        # 15 balanced cards with varying damage
        self.cards = [
            Card("Light Hit", 10),
            Card("Quick Slash", 15),
            Card("Strike", 20),
            Card("Heavy Blow", 25),
            Card("Power Hit", 30),
            Card("Light Hit", 10),
            Card("Quick Slash", 15),
            Card("Strike", 20),
            Card("Heavy Blow", 25),
            Card("Power Hit", 30),
            Card("Strong Attack", 35),
            Card("Mighty Blow", 40),
            Card("Critical", 45),
            Card("Devastating", 50),
            Card("ULTIMATE", 60),
        ]
    
    def create_card_buttons(self):
        for i, card in enumerate(self.cards):
            btn = Button(
                text=f"{card.name}\n⚔️ {card.damage}",
                size_hint=(None, None),
                size=(150, 100),
                font_size='18sp',
                bold=True
            )
            
            # Color based on damage
            if card.damage >= 50:
                btn.background_color = (0.8, 0.1, 0.1, 1)  # Dark red - ultimate
            elif card.damage >= 40:
                btn.background_color = (1, 0.3, 0.3, 1)  # Red - strong
            elif card.damage >= 30:
                btn.background_color = (1, 0.6, 0.2, 1)  # Orange - medium
            elif card.damage >= 20:
                btn.background_color = (1, 0.9, 0.3, 1)  # Yellow - normal
            else:
                btn.background_color = (0.3, 0.8, 0.3, 1)  # Green - weak
            
            btn.bind(on_press=lambda instance, c=card, idx=i: self.play_card(c, idx))
            self.card_layout.add_widget(btn)
    
    def play_card(self, card, card_idx):
        if self.game_over:
            return
        
        # Play the card
        result = self.battle.play_card(card.damage)
        
        # Calculate remaining cards (inverse index because layout is reversed)
        cards_remaining = len(self.card_layout.children) - 1
        
        # Update UI
        self.boss_label.text = f"👹 BOSS: {max(0, self.battle.boss_hp)}/{self.battle.boss_max_hp}"
        self.player_label.text = f"❤️ YOU: {max(0, self.battle.player_hp)}/{self.battle.player_max_hp}"
        self.cards_label.text = f"Cards: {cards_remaining}"
        
        # Battle message
        if result == "playing":
            self.battle_area.text = f"⚡ Used {card.name}!\nDealt {card.damage} damage!\nBoss hits back for {self.battle.boss_damage}!"
        elif result == "win":
            self.battle_area.text = f"⚡ {card.name} deals {card.damage} damage!\n🎉 BOSS DEFEATED! 🎉"
        elif result == "lose":
            self.battle_area.text = f"⚡ {card.name} deals {card.damage} damage!\n💀 YOU DIED... 💀"
        
        # Remove the card button (handle index carefully)
        children = self.card_layout.children
        # Find and remove the correct button
        for child in children:
            if hasattr(child, 'text') and card.name in child.text:
                self.card_layout.remove_widget(child)
                break
        
        # Check win/lose
        if result == "win":
            self.game_over = True
            self.show_win()
        elif result == "lose":
            self.game_over = True
            self.show_lose()
    
    def show_win(self):
        self.boss_label.color = (0, 1, 0, 1)
        self.battle_area.color = (0, 1, 0, 1)
        self.battle_area.font_size = '28sp'
        self.add_restart_button("VICTORY!")
    
    def show_lose(self):
        self.player_label.color = (1, 0, 0, 1)
        self.battle_area.color = (1, 0.2, 0.2, 1)
        self.battle_area.font_size = '28sp'
        self.add_restart_button("TRY AGAIN")
    
    def add_restart_button(self, button_text):
        restart_btn = Button(
            text=button_text,
            size_hint_y=0.1,
            font_size='24sp',
            bold=True,
            background_color=(0.2, 0.6, 1, 1)
        )
        restart_btn.bind(on_press=self.restart)
        self.add_widget(restart_btn)
    
    def restart(self, instance):
        # Reset game state
        self.battle.reset()
        self.game_over = False
        
        # Clear all widgets and rebuild
        self.clear_widgets()
        
        # Reset colors
        self.boss_label.color = (1, 0.3, 0.3, 1)
        self.player_label.color = (0.3, 1, 0.3, 1)
        self.battle_area.color = (0.9, 0.9, 0.9, 1)
        self.battle_area.font_size = '22sp'
        
        # Rebuild UI
        self.build_ui()

# ========== MAIN APP ==========
class BossBattleApp(App):
    def build(self):
        self.title = "Boss Battle - Card Game"
        return GameScreen()

if __name__ == '__main__':
    BossBattleApp().run()