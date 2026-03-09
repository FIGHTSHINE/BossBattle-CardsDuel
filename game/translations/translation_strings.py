"""Translation strings aggregator - combines all translation categories."""

from .ui_translations import UITranslations
from .message_translations import MessageTranslations
from .menu_translations import MenuTranslations
from .log_translations import LogTranslations


class Translations:
    """Combined translation strings from all categories."""
    
    # UI translations
    
    UI_TURN_PLAYER = UITranslations.TURN_PLAYER
    UI_TURN_BOSS = UITranslations.TURN_BOSS
    UI_BOSS_HP = UITranslations.BOSS_HP
    UI_PLAYER_HP = UITranslations.PLAYER_HP
    UI_SHIELD_UP = UITranslations.SHIELD_UP
    UI_CARDS_THIS_TURN = UITranslations.CARDS_THIS_TURN
    UI_END_TURN = UITranslations.END_TURN
    UI_BATTLE_AREA_START = UITranslations.BATTLE_AREA_START
    UI_TURN_COUNTER = UITranslations.TURN_COUNTER
    UI_BOSS_WARNING = UITranslations.BOSS_WARNING
    UI_CARDS_REMAINING = UITranslations.CARDS_REMAINING
    UI_CARDS_DECK_EMPTY = UITranslations.CARDS_DECK_EMPTY
    UI_DECK_NO_CARDS = UITranslations.DECK_NO_CARDS
    UI_DECK_EMPTY_WARNING = UITranslations.DECK_EMPTY_WARNING
    UI_DECK_LAST_DRAW = UITranslations.DECK_LAST_DRAW
    UI_VICTORY_TURNS = UITranslations.VICTORY_TURNS
    UI_DEFEAT_TURNS = UITranslations.DEFEAT_TURNS
    UI_PLAY_AGAIN = UITranslations.PLAY_AGAIN
    
    # Button translations
    BTN_PLAY_AGAIN = UITranslations.PLAY_AGAIN
    BTN_TRY_AGAIN = UITranslations.TRY_AGAIN
    MENU_BACK_TO_MAIN = UITranslations.BACK_TO_MAIN
    
    # Message translations
    MSG_VICTORY = MessageTranslations.VICTORY
    MSG_DEFEAT = MessageTranslations.DEFEAT
    MSG_ATTACK = MessageTranslations.ATTACK
    MSG_CRITICAL_HIT = MessageTranslations.CRITICAL_HIT
    MSG_HEAL = MessageTranslations.HEAL
    MSG_BOSS_ATTACK_BLOCKED = MessageTranslations.BOSS_ATTACK_BLOCKED
    MSG_BOSS_ATTACK_BLOCKED_PARTIAL = MessageTranslations.BOSS_ATTACK_BLOCKED_PARTIAL
    MSG_BOSS_ATTACK_NO_SHIELD = MessageTranslations.BOSS_ATTACK_NO_SHIELD
    MSG_SHIELD_UP = MessageTranslations.SHIELD_UP
    MSG_BOSS_SPECIAL_BLOCKED = MessageTranslations.BOSS_SPECIAL_ATTACK_BLOCKED
    MSG_BOSS_SPECIAL_BLOCKED_PARTIAL = MessageTranslations.BOSS_SPECIAL_ATTACK_BLOCKED_PARTIAL  # ✅ 添加这行
    MSG_BOSS_SPECIAL_PARTIAL = MessageTranslations.BOSS_SPECIAL_ATTACK_PARTIAL
    MSG_BOSS_SPECIAL_NO_SHIELD = MessageTranslations.BOSS_SPECIAL_ATTACK_NO_SHIELD
    MSG_ERROR_END_TURN = MessageTranslations.ERROR_END_TURN
    MSG_ERROR_SPECIAL_ATTACK = MessageTranslations.ERROR_SPECIAL_ATTACK
    MSG_ERROR_GAME_OVER = MessageTranslations.ERROR_GAME_OVER
    MSG_ERROR_CANNOT_PLAY = MessageTranslations.ERROR_CANNOT_PLAY_NOW
    MSG_ERROR_NOT_TURN = MessageTranslations.ERROR_NOT_PLAYER_TURN

    # Menu translations
    MENU_TITLE = MenuTranslations.TITLE
    MENU_SELECT_MODE = MenuTranslations.SELECT_MODE
    MENU_MODE_BOSS_DUEL = MenuTranslations.MODE_BOSS_DUEL
    MENU_MODE_SURVIVAL = MenuTranslations.MODE_SURVIVAL
    MENU_MODE_PVP = MenuTranslations.MODE_PVP
    MENU_OPTIONS = MenuTranslations.OPTIONS
    MENU_LANGUAGE = MenuTranslations.LANGUAGE
    MENU_ABOUT = MenuTranslations.ABOUT
    MENU_ABOUT_TITLE = MenuTranslations.ABOUT_TITLE
    MENU_ABOUT_CONTENT = MenuTranslations.ABOUT_CONTENT
    MENU_EXIT = MenuTranslations.EXIT
    
    # ✅ Game Mode Rules
    MODE_RULES_BOSS_DUEL = MenuTranslations.MODE_RULES_BOSS_DUEL
    MODE_RULES_SURVIVAL = MenuTranslations.MODE_RULES_SURVIVAL
    MODE_RULES_PVP = MenuTranslations.MODE_RULES_PVP
    
    # ✅ Popup buttons and titles
    POPUP_CONFIRM = MenuTranslations.POPUP_CONFIRM
    POPUP_BACK = MenuTranslations.POPUP_BACK
    POPUP_TITLE_RULES = MenuTranslations.POPUP_TITLE_RULES
    
    # Language selection
    LANG_SELECT_TITLE = MenuTranslations.LANG_SELECT_TITLE
    LANG_BTN_ZH = MenuTranslations.LANG_BTN_ZH
    LANG_BTN_EN = MenuTranslations.LANG_BTN_EN
    UI_MUTE_ON = MenuTranslations.UI_MUTE_ON
    UI_MUTE_OFF = MenuTranslations.UI_MUTE_OFF

    # Log translations
    LOG_BATTLE_INIT = LogTranslations.BATTLE_INIT
    LOG_BATTLE_INIT_COMPLETE = LogTranslations.BATTLE_INIT_COMPLETE
    LOG_BOSS_HP = LogTranslations.BOSS_HP
    LOG_PLAYER_HP = LogTranslations.PLAYER_HP
    LOG_BOSS_DAMAGE = LogTranslations.BOSS_DAMAGE
    LOG_MAX_CARDS = LogTranslations.MAX_CARDS