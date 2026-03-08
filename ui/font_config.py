"""Font configuration for multi-language text support."""

from kivy.core.text import LabelBase
from kivy.utils import platform
import os

# Global font name
_chinese_font_name = None

def register_chinese_fonts():
    """Register Chinese fonts for Kivy (cross-platform)."""
    global _chinese_font_name
    
    try:
        print(f"[FONT] ========================================")
        print(f"[FONT] Starting font registration...")
        print(f"[FONT] Platform: {platform}")
        
        # ✅ 平台检测
        if platform == 'android':
            # Android: 使用系统字体
            _register_android_fonts()
        elif platform == 'windows' or platform == 'win':
            # Windows: 使用系统字体
            _register_windows_fonts()
        elif platform == 'ios':
            # iOS: 使用系统字体
            _register_ios_fonts()
        elif platform == 'macosx':
            # macOS: 使用系统字体
            _register_macos_fonts()
        else:
            # Linux 或其他平台
            _register_linux_fonts()
        
        # ✅ 确保总是有字体名称（即使注册失败）
        if _chinese_font_name is None:
            _chinese_font_name = 'Roboto'
            print(f"[FONT] ⚠️ No Chinese font found, using default: {_chinese_font_name}")
        else:
            print(f"[FONT] ✅ Successfully registered font: {_chinese_font_name}")
        
        print(f"[FONT] Final font name: {_chinese_font_name}")
        print(f"[FONT] ========================================")
        
        return _chinese_font_name
        
    except Exception as e:
        print(f"[FONT] ❌ Error registering Chinese font: {e}")
        import traceback
        traceback.print_exc()
        # ✅ 异常时也返回默认字体
        _chinese_font_name = 'Roboto'
        return _chinese_font_name

def _register_windows_fonts():
    """Register fonts on Windows."""
    global _chinese_font_name
    
    print(f"[FONT] Checking Windows fonts...")
    
    windows_fonts = [
        ('C:/Windows/Fonts/msyh.ttc', 'msyh'),      # 微软雅黑
        ('C:/Windows/Fonts/simhei.ttf', 'simhei'),    # 黑体
        ('C:/Windows/Fonts/simsun.ttc', 'simsun'),    # 宋体
        ('C:/Windows/Fonts/msyhbd.ttc', 'msyhbd'),    # 微软雅黑粗体
    ]
    
    for font_path, font_name in windows_fonts:
        exists = os.path.exists(font_path)
        print(f"[FONT]   Checking: {font_path} - {'✓ Found' if exists else '✗ Not found'}")
        
        if exists:
            try:
                LabelBase.register(name=font_name, fn_regular=font_path)
                _chinese_font_name = font_name
                print(f"[FONT] ✅ Registered: {font_name} from {font_path}")
                return
            except Exception as e:
                print(f"[FONT] ❌ Failed to register {font_name}: {e}")
                continue
    
    # ✅ 如果没有找到任何字体
    print(f"[FONT] ⚠️ No Windows Chinese fonts found!")
    # 不要在这里设置 _chinese_font_name，让调用者处理

def _register_android_fonts():
    """Register fonts on Android using system fonts."""
    global _chinese_font_name
    
    print(f"[FONT] Checking Android fonts...")
    
    # Android 系统中文字体路径
    android_system_fonts = [
        '/system/fonts/NotoSansCJK-Regular.ttc',
        '/system/fonts/NotoSansSC-Regular.otf',
        '/system/fonts/DroidSansFallback.ttf',
    ]
    
    for font_path in android_system_fonts:
        try:
            if os.path.exists(font_path):
                LabelBase.register(name='chinese_font', fn_regular=font_path)
                _chinese_font_name = 'chinese_font'
                print(f"[FONT] ✅ Android font: {font_path}")
                return
        except Exception as e:
            print(f"[FONT] ❌ Failed to load {font_path}: {e}")
            continue
    
    print(f"[FONT] ⚠️ No Android Chinese fonts found")

def _register_macos_fonts():
    """Register fonts on macOS."""
    global _chinese_font_name
    
    print(f"[FONT] Checking macOS fonts...")
    
    macos_fonts = [
        ('/System/Library/Fonts/PingFang.ttc', 'pingfang'),
        ('/Library/Fonts/Arial Unicode.ttf', 'arial_unicode'),
    ]
    
    for font_path, font_name in macos_fonts:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name=font_name, fn_regular=font_path)
                _chinese_font_name = font_name
                print(f"[FONT] ✅ macOS font: {font_name}")
                return
            except Exception as e:
                print(f"[FONT] ❌ Failed to register {font_path}: {e}")
                continue
    
    print(f"[FONT] ⚠️ No macOS Chinese fonts found")

def _register_ios_fonts():
    """Register fonts on iOS."""
    global _chinese_font_name
    
    print(f"[FONT] Checking iOS fonts...")
    
    try:
        LabelBase.register(name='pingfang', fn_regular='/System/Library/Fonts/PingFang.ttc')
        _chinese_font_name = 'pingfang'
        print(f"[FONT] ✅ iOS font: PingFang")
        return
    except Exception as e:
        print(f"[FONT] ❌ Failed to register iOS font: {e}")

def _register_linux_fonts():
    """Register fonts on Linux."""
    global _chinese_font_name
    
    print(f"[FONT] Checking Linux fonts...")
    
    linux_fonts = [
        ('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 'wqy'),
        ('/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc', 'noto'),
    ]
    
    for font_path, font_name in linux_fonts:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name=font_name, fn_regular=font_path)
                _chinese_font_name = font_name
                print(f"[FONT] ✅ Linux font: {font_name}")
                return
            except Exception as e:
                print(f"[FONT] ❌ Failed to register {font_path}: {e}")
                continue
    
    print(f"[FONT] ⚠️ No Linux Chinese fonts found")

def get_chinese_font_name():
    """
    Get the registered Chinese font name.
    
    Returns:
        str: Font name (never None, always returns a valid font name)
    """
    global _chinese_font_name
    
    # ✅ 强制保护：如果为 None，立即设置默认值
    if _chinese_font_name is None:
        print(f"[FONT] ⚠️ Warning: _chinese_font_name is None, using 'Roboto'")
        _chinese_font_name = 'Roboto'
    
    # ✅ 再次确保（双重保险）
    if not _chinese_font_name or _chinese_font_name == 'None':
        print(f"[FONT] ⚠️ Warning: Invalid font name, using 'Roboto'")
        _chinese_font_name = 'Roboto'
    
    return _chinese_font_name

def init_fonts():
    """
    Initialize fonts for the application.
    Call this in App.build() to ensure fonts are registered before UI is created.
    """
    global _chinese_font_name
    
    print(f"[FONT] ========================================")
    print(f"[FONT] init_fonts() called")
    
    # 先尝试注册字体
    result = register_chinese_fonts()
    
    # ✅ 强制保护：确保全局变量永远不为 None
    if _chinese_font_name is None:
        _chinese_font_name = 'Roboto'
        print(f"[FONT] ⚠️ Force set to 'Roboto' (was None)")
    
    # 再次确认
    if result is None:
        result = 'Roboto'
        print(f"[FONT] init_fonts: Using default font 'Roboto'")
    
    # 三重保险
    if _chinese_font_name != result:
        print(f"[FONT] ⚠️ Mismatch detected, syncing...")
        _chinese_font_name = result
    
    print(f"[FONT] Final font name: {_chinese_font_name}")
    print(f"[FONT] ========================================")
    
    return result

# ✅ 注释掉模块加载时的自动注册
# register_chinese_fonts()