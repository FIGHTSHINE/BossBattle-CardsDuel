"""UI logging system for debug and monitoring."""

import traceback


class UILogger:
    """Centralized logging system for UI events."""
    
    @staticmethod
    def log_separator():
        """Print a separator line."""
        print("=" * 50)
    
    @staticmethod
    def log_init():
        """Log game screen initialization."""
        print("\n" + "=" * 50)
        print("[GameScreen] Initializing game screen...")
    
    @staticmethod
    def log_init_success():
        """Log successful initialization."""
        print("[GameScreen] Game screen initialized successfully!")
        print("=" * 50 + "\n")
    
    @staticmethod
    def log_ui_build_start():
        """Log UI build start."""
        print("[UI] Building user interface components...")
    
    @staticmethod
    def log_ui_component_added(component_name):
        """Log UI component addition."""
        print(f"[UI] ✓ {component_name} added")
    
    @staticmethod
    def log_ui_build_complete():
        """Log UI build completion."""
        print("[UI] User interface build complete!")
    
    @staticmethod
    def log_deck_create_start():
        """Log deck creation start."""
        print(f"\n[DECK] Creating card deck...")
    
    @staticmethod
    def log_deck_created(count):
        """Log deck creation success."""
        print(f"[DECK] ✓ Deck created with {count} cards")
    
    @staticmethod
    def log_card_buttons_create_start(total):
        """Log card buttons creation start."""
        print(f"[UI] Creating {total} card buttons...")
    
    @staticmethod
    def log_card_buttons_progress(current, total):
        """Log card buttons creation progress."""
        if current % 5 == 0:
            print(f"[UI]   Created {current}/{total} card buttons...")
    
    @staticmethod
    def log_card_buttons_complete(total):
        """Log card buttons creation success."""
        print(f"[UI] ✓ All {total} card buttons created successfully")
    
    @staticmethod
    def log_card_clicked(card_name):
        """Log card click event."""
        print(f"\n[UI] Player clicked card: {card_name}")
    
    @staticmethod
    def log_card_blocked_game_over():
        """Log card play blocked by game over."""
        print(f"[UI] Card play blocked: Game is over")
    
    @staticmethod
    def log_card_blocked_cannot_play():
        """Log card play blocked by game rules."""
        print(f"[UI] Card play blocked: Cannot play card (see BattleManager logs)")
    
    @staticmethod
    def log_ui_update_start():
        """Log UI update start."""
        print(f"[UI] Updating UI elements...")
    
    @staticmethod
    def log_ui_update_success():
        """Log UI update success."""
        print(f"[UI] ✓ UI updated successfully")
    
    @staticmethod
    def log_damage_animation():
        """Log damage animation."""
        print(f"[UI] Playing damage flash animation...")
    
    @staticmethod
    def log_low_hp_warning(hp):
        """Log low HP warning."""
        print(f"[UI] ⚠️ Low HP warning! Player HP: {hp}")
    
    @staticmethod
    def log_counter_update(cards_played, max_cards):
        """Log cards played counter update."""
        print(f"[UI] Cards played counter updated: {cards_played}/{max_cards}")
    
    @staticmethod
    def log_max_cards_reached(max_cards):
        """Log max cards reached."""
        print(f"[UI] Max cards reached ({max_cards}), disabling all cards...")
    
    @staticmethod
    def log_end_turn_clicked():
        """Log end turn button click."""
        print(f"\n[UI] 'END TURN' button clicked")
    
    @staticmethod
    def log_end_turn_blocked_game_over():
        """Log end turn blocked by game over."""
        print(f"[UI] End turn blocked: Game is over")
    
    @staticmethod
    def log_end_turn_blocked_not_player_turn(current_turn):
        """Log end turn blocked by wrong turn."""
        print(f"[UI] End turn blocked: Not player's turn (current: {current_turn})")
    
    @staticmethod
    def log_boss_turn_start():
        """Log boss turn start."""
        print(f"[UI] Executing boss turn...")
    
    @staticmethod
    def log_boss_turn_update_ui():
        """Log boss turn UI update."""
        print(f"[UI] Updating UI after boss attack...")
    
    @staticmethod
    def log_game_continues():
        """Log game continues."""
        print(f"[UI] Game continues, re-enabling cards...")
    
    @staticmethod
    def log_cards_re_enabled():
        """Log cards re-enabled."""
        print(f"[UI] ✓ Cards re-enabled, counter reset")
    
    @staticmethod
    def log_turn_indicator_player():
        """Log turn indicator update to player."""
        print(f"[UI] Turn indicator updated: YOUR TURN (green)")
    
    @staticmethod
    def log_turn_indicator_boss():
        """Log turn indicator update to boss."""
        print(f"[UI] Turn indicator updated: BOSS TURN (red)")
    
    @staticmethod
    def log_disabling_cards():
        """Log disabling all cards."""
        print(f"[UI] Disabling all card buttons...")
    
    @staticmethod
    def log_cards_disabled(count):
        """Log cards disabled."""
        print(f"[UI] ✓ Disabled {count} card buttons")
    
    @staticmethod
    def log_enabling_cards():
        """Log enabling all cards."""
        print(f"[UI] Enabling all card buttons...")
    
    @staticmethod
    def log_cards_enabled(count):
        """Log cards enabled."""
        print(f"[UI] ✓ Enabled {count} card buttons")
    
    @staticmethod
    def log_removing_card(card_name):
        """Log card removal."""
        print(f"[UI] Removing card widget: {card_name}")
    
    @staticmethod
    def log_card_removed():
        """Log card removal success."""
        print(f"[UI] ✓ Card widget removed successfully")
    
    @staticmethod
    def log_card_not_found():
        """Log card not found warning."""
        print(f"[UI] ⚠️ Card widget not found in card_widgets dictionary")
    
    @staticmethod
    def log_win(turns):
        """Log victory."""
        print(f"\n[GAME] " + "=" * 50)
        print(f"[GAME] 🎉 VICTORY! 🎉")
        print(f"[GAME] Boss defeated in {turns} turns!")
        print(f"[GAME] " + "=" * 50)
    
    @staticmethod
    def log_lose(turns):
        """Log defeat."""
        print(f"\n[GAME] " + "=" * 50)
        print(f"[GAME] 💀 DEFEAT 💀")
        print(f"[GAME] Survived {turns} turns...")
        print(f"[GAME] " + "=" * 50)
    
    @staticmethod
    def log_win_screen_displayed():
        """Log win screen displayed."""
        print(f"[UI] ✓ Win screen displayed")
    
    @staticmethod
    def log_lose_screen_displayed():
        """Log lose screen displayed."""
        print(f"[UI] ✓ Lose screen displayed")
    
    @staticmethod
    def log_restart_button_added(button_text):
        """Log restart button added."""
        print(f"[UI] Adding restart button: '{button_text}'")
    
    @staticmethod
    def log_restart_button_added_success():
        """Log restart button added success."""
        print(f"[UI] ✓ Restart button added")
    
    @staticmethod
    def log_restart_clicked():
        """Log restart button click."""
        print(f"\n[UI] 'RESTART' button clicked")
    
    @staticmethod
    def log_restart_resetting():
        """Log restart resetting."""
        print(f"[UI] Resetting game state...")
    
    @staticmethod
    def log_restart_clear_widgets():
        """Log restart clearing widgets."""
        print(f"[UI] Clearing all widgets...")
    
    @staticmethod
    def log_restart_rebuild_ui():
        """Log restart rebuilding UI."""
        print(f"[UI] Rebuilding UI...")
    
    @staticmethod
    def log_reset_complete():
        """Log restart complete."""
        print(f"[UI] ✓ Game reset complete!")
    
    @staticmethod
    def log_error(location, exception):
        """Log error with traceback."""
        print(f"[ERROR] Exception in {location}: {type(exception).__name__}: {exception}")
        traceback.print_exc()
    
    @staticmethod
    def log_error_no_traceback(location, exception):
        """Log error without traceback."""
        print(f"[ERROR] Exception in {location}: {type(exception).__name__}: {exception}")