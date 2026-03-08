"""Hand card display component."""

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

from ui.ui_logger import UILogger


class HandDisplay(BoxLayout):
    """Displays player's hand cards."""
    
    def __init__(self, card_play_callback, **kwargs):
        """
        Initialize hand display.
        
        Args:
            card_play_callback: Function to call when card is played
        """
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = 0.5
        
        self.card_play_callback = card_play_callback
        self.card_widgets = {}
        self.logger = UILogger()
        
        # Create scroll area for cards
        self.scroll = ScrollView(
            size_hint_y=1,
            bar_width='10sp'
        )
        
        self.layout = BoxLayout(
            size_hint_y=None,
            spacing='8sp',
            padding='10sp'
        )
        self.layout.bind(minimum_height=self.layout.setter('height'))
        
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)
    
    def display_hand(self, cards, builder):
        """
        Display cards in hand.
        
        Args:
            cards: List of Card objects
            builder: UIBuilder instance to create card buttons
        """
        print(f"\n[HandDisplay] Displaying {len(cards)} cards")
        
        # Clear existing cards
        self.layout.clear_widgets()
        self.card_widgets.clear()
        
        # Create button for each card
        for card in cards:
            btn = builder.build_card_button(card, self.card_play_callback)
            self.layout.add_widget(btn)
            self.card_widgets[card.unique_id] = btn
            print(f"[HandDisplay]   Added: {card.name}")
    
    def remove_card(self, card):
        """
        Remove a card from display.
        
        Args:
            card: Card object to remove
        """
        if card.unique_id in self.card_widgets:
            widget = self.card_widgets[card.unique_id]
            if widget in self.layout.children:
                self.layout.remove_widget(widget)
            del self.card_widgets[card.unique_id]
            print(f"[HandDisplay] Removed: {card.name}")
    
    def enable_all(self):
        """Enable all card buttons."""
        for widget in self.card_widgets.values():
            widget.disabled = False
    
    def disable_all(self):
        """Disable all card buttons."""
        for widget in self.card_widgets.values():
            widget.disabled = True