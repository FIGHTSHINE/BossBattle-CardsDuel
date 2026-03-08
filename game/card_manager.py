"""Card drawing and hand management system."""

import random
from game.deck import Deck


class CardManager:
    """Manages deck, hand, and card drawing."""
    
    def __init__(self, max_hand_size=5):
        """Initialize card manager with shuffled deck."""
        self.max_hand_size = max_hand_size
        
        # Create and shuffle full deck (20 cards)
        self.draw_pile = Deck.create_balanced_deck()
        random.shuffle(self.draw_pile)
        
        print(f"[CardManager] Deck initialized: {len(self.draw_pile)} cards")
        
        # Player's hand (cards currently available)
        self.hand = []
        
        # Discard pile (played cards - NOT reshuffled anymore!)
        self.discard_pile = []
        
        # Draw initial hand
        self.draw_initial_hand()
    
    def draw_initial_hand(self):
        """Draw initial hand (max_hand_size cards)."""
        print(f"[CardManager] Drawing initial hand ({self.max_hand_size} cards)...")
        
        for _ in range(self.max_hand_size):
            if self.draw_pile:
                self.hand.append(self.draw_pile.pop())
            else:
                print(f"[CardManager] ⚠️ Deck has fewer than {self.max_hand_size} cards!")
                break
        
        print(f"[CardManager] Initial hand: {len(self.hand)} cards")
        self.log_status()
    
    def refill_hand(self, max_draws=None):
        """
        Draw cards with turn-based limit.
        
        Args:
            max_draws: Maximum number of cards to draw this turn.
                      If None, fills hand to max_hand_size (default behavior).
        
        Returns: (number_of_cards_drawn, is_deck_empty)
        """
        current = len(self.hand)
        
        if max_draws is not None:
            #  hand limit： draw max_draws cards per turn, even if hand is not full
            can_draw = max_draws
            actual_draw = min(can_draw, self.max_hand_size - current)
        else:
            # default behavior: fill hand to max_hand_size
            needed = self.max_hand_size - current
            actual_draw = needed
        
        cards_drawn = 0
        is_deck_empty = False
        
        if actual_draw > 0:
            print(f"[CardManager] Drawing up to {actual_draw} card(s)...")
            
            for _ in range(actual_draw):
                if not self.draw_pile:
                    print(f"[CardManager] ⚠️ Draw pile is empty! Cannot draw more cards.")
                    is_deck_empty = True
                    break
                
                self.hand.append(self.draw_pile.pop())
                cards_drawn += 1
            
            if cards_drawn > 0:
                if is_deck_empty:
                    print(f"[CardManager] Drew the last {cards_drawn} card(s) from deck.")
                else:
                    print(f"[CardManager] Drew {cards_drawn} card(s).")
            
            self.log_status()
        
        return cards_drawn, is_deck_empty
    
    def play_card(self, card):
        """Remove card from hand and add to discard (permanent)."""
        if card in self.hand:
            self.hand.remove(card)
            self.discard_pile.append(card)
            print(f"[CardManager] Played: {card.name} | Hand: {len(self.hand)}/{self.max_hand_size} | Discard: {len(self.discard_pile)}")
            return True
        
        print(f"[CardManager] ⚠️ Card {card.name} not in hand!")
        return False
    
    def get_hand(self):
        """Get current hand."""
        return self.hand.copy()
    
    def get_hand_size(self):
        """Get current hand size."""
        return len(self.hand)
    
    def cards_total_remaining(self):
        """Get total cards remaining (hand + draw pile)."""
        return len(self.hand) + len(self.draw_pile)
    
    def is_draw_pile_empty(self):
        """Check if draw pile is empty."""
        return len(self.draw_pile) == 0
    
    def is_completely_empty(self):
        """Check if both draw pile and hand are empty."""
        return len(self.draw_pile) == 0 and len(self.hand) == 0
    
    def log_status(self):
        """Print current status."""
        print(f"[CardManager] Hand: {len(self.hand)}/{self.max_hand_size} | Draw: {len(self.draw_pile)} | Discard: {len(self.discard_pile)}")