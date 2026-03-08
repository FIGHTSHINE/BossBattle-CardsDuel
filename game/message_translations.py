"""Game message translations."""

class MessageTranslations:
    """Game message translation strings."""
    
    # Victory/Defeat
    VICTORY = {
        'zh': "🎉 胜利! 🎉\n在第{}回合击败了Boss!",
        'en': "🎉 VICTORY! 🎉\nBoss defeated in {} turns!"
    }
    
    DEFEAT = {
        'zh': " 失败 💀\n坚持了{}回合...",
        'en': " DEFEATED 💀\nSurvived {} turns..."
    }
    
    # Card effects
    ATTACK = {
        'zh': " 使用了{}! 造成{}点伤害!",
        'en': " Used {}! Dealt {} damage!"
    }
    
    CRITICAL_HIT = {
        'zh': " 暴击! {}造成{}点伤害!",
        'en': " CRITICAL HIT! {} deals {} damage!"
    }
    
    HEAL = {
        'zh': "恢复了{}点生命值!",
        'en': "Healed {} HP!"
    }
    
    SHIELD_UP = {
        'zh': " 护盾激活! 可阻挡{}点伤害!",
        'en': " Shield up! Blocks {} damage!"
    }
    
    # Boss attack messages
    BOSS_ATTACK_BLOCKED = {
        'zh': " Boss攻击! 护盾格挡了{}点伤害!",
        'en': " Boss attacks! Blocked {}!"
    }
    
    BOSS_ATTACK_BLOCKED_PARTIAL = {
        'zh': " Boss攻击! 护盾格挡了{}点伤害! 受到{}点伤害!",
        'en': " Boss attacks! Blocked {}! Took {} damage!"
    }
    
    BOSS_ATTACK_NO_SHIELD = {
        'zh': " Boss攻击! 受到{}点伤害!",
        'en': " Boss attacks! Took {} damage!"
    }

    # Boss大招消息
    BOSS_SPECIAL_ATTACK_BLOCKED = {
        'zh': "🔥 Boss大招! 🔥 护盾格挡了{}点伤害!",
        'en': "🔥 BOSS SPECIAL ATTACK! 🔥 Blocked {} damage!"
    }
    
    # ✅ 添加：Boss大招部分格挡（2个参数）
    BOSS_SPECIAL_ATTACK_BLOCKED_PARTIAL = {
        'zh': "🔥 Boss大招! 🔥 护盾格挡了{}点伤害! 受到{}点伤害!",
        'en': "🔥 BOSS SPECIAL ATTACK! 🔥 Blocked {} damage! Took {} damage!"
    }

    BOSS_SPECIAL_ATTACK_PARTIAL = {
        'zh': "受到{}点伤害!",
        'en': "Took {} damage!"
    }

    BOSS_SPECIAL_ATTACK_NO_SHIELD = {
        'zh': "🔥 Boss大招! 🔥 受到{}点伤害!",
        'en': "🔥 BOSS SPECIAL ATTACK! 🔥 Took {} damage!"
    }
    # 错误消息
    ERROR_END_TURN = {
        'zh': "结束回合时出错: {}",
        'en': "Error ending turn: {}"
    }

    ERROR_SPECIAL_ATTACK = {
        'zh': "大招执行出错: {}",
        'en': "Error in special attack: {}"
    }
    # 游戏控制错误
    ERROR_GAME_OVER = {
        'zh': "游戏已结束",
        'en': "Game is over"
    }
    
    ERROR_CANNOT_PLAY_NOW = {
        'zh': "现在无法出牌",
        'en': "Cannot play card now"
    }
    
    ERROR_NOT_PLAYER_TURN = {
        'zh': "不是玩家回合",
        'en': "Not player turn"
    }