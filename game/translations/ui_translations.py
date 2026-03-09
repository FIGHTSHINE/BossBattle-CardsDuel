"""UI element translations."""

class UITranslations:
    """UI element translation strings."""
    
    # 回合信息
    TURN_COUNTER = {
        'zh': "第{}回合",
        'en': "Turn: {}"
    }
    
    TURN_PLAYER = {
        'zh': " 你的回合",
        'en': " YOUR TURN"
    }
    
    TURN_BOSS = {
        'zh': " Boss的回合",
        'en': " BOSS TURN"
    }

    # Boss警告
    BOSS_WARNING = {
        'zh': " Boss狂暴!大招已准备就绪!",
        'en': " BOSS ENRAGED!SPECIAL ATTACK READY!"
    }

    # HP displays
    BOSS_HP = {
        'zh': " Boss: {}/{}",
        'en': " BOSS: {}/{}"
    }
    
    PLAYER_HP = {
        'zh': " 你: {}/{}",
        'en': " YOU: {}/{}"
    }
    
    SHIELD_UP = {
        'zh': " 护盾: {}",
        'en': " Shield: {}"
    }
    
    # 卡牌信息
    CARDS_REMAINING = {
        'zh': "手牌: {} | 牌库: {} | 已用: {}",
        'en': "Hand: {} | Deck: {} | Used: {}"
    }

    CARDS_DECK_EMPTY = {
        'zh': "手牌: {} | 牌库: 空 | 已用: {}",
        'en': "Hand: {} | Deck: EMPTY | Used: {}"
    }

    CARDS_THIS_TURN = {
        'zh': "本回合出牌: {}/{}",
        'en': "Cards this turn: {}/{}"
    }

    # 胜负消息
    VICTORY_TURNS = {
        'zh': "在{}回合内击败了Boss!",
        'en': "Boss defeated in {} turns!"
    }

    DEFEAT_TURNS = {
        'zh': "坚持了{}回合...",
        'en': "Survived {} turns..."
    }

    # 牌库警告
    DECK_NO_CARDS = {
        'zh': " 手牌已空!",
        'en': " NO CARDS LEFT!\nFinal battle with empty hand!"
    }

    DECK_EMPTY_WARNING = {
        'zh': " 牌库已空!\n剩余{}张手牌。",
        'en': " Deck empty!\n{} card(s) remaining."
    }

    DECK_LAST_DRAW = {
        'zh': " 抽取了最后{}张牌!",
        'en': " Last {} card(s) drawn!"
    }
    
    # Buttons
    END_TURN = {
        'zh': "结束回合",
        'en': "END TURN"
    }
    
    PLAY_AGAIN = {
        'zh': "再玩一次",
        'en': "PLAY AGAIN"
    }
    
    TRY_AGAIN = {
        'zh': "重新挑战",
        'en': "TRY AGAIN"
    }
    
    BACK_TO_MAIN = {
        'zh': " 主菜单",
        'en': " Main Menu"
    }
    
    # Battle area
    BATTLE_AREA_START = {
        'zh': "选择一张卡牌进行攻击!",
        'en': "Choose a card to attack!"
    }