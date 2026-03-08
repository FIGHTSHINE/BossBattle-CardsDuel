"""Language selection screen."""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from game.translations import language_manager
from ui.font_config import get_chinese_font_name  # ✅ 添加导入


class LanguageSelectScreen(BoxLayout):
    """Screen for selecting game language."""
    
    def __init__(self, on_language_selected, **kwargs):
        """Initialize language select screen."""
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = '50sp'
        self.spacing = '20sp'
        
        self.on_language_selected = on_language_selected
        
        # ✅ 获取字体名称
        self.chinese_font = get_chinese_font_name()
        
        # ✅ 运行时保护
        if self.chinese_font is None:
            print("[LangSelect] ❌ CRITICAL: Font is None, forcing to 'Roboto'")
            self.chinese_font = 'Roboto'
        
        print(f"[LangSelect] ✅ Using font: '{self.chinese_font}'")
        self.build_ui()
    
    def build_ui(self):
        """Build the language selection UI."""
        # Title
        title = Label(
            text="🌍 语言选择 / Select Language 🌍",
            font_size='32sp',
            size_hint_y=0.3,
            color=(0.3, 0.8, 1, 1),
            bold=True,
            font_name=self.chinese_font or 'Roboto'  # ✅ 添加中文字体
        )
        self.add_widget(title)
        
        # Spacer
        spacer = Label(
            text="",
            size_hint_y=0.2,
            font_name=self.chinese_font or 'Roboto'  # ✅ 添加中文字体
        )
        self.add_widget(spacer)
        
        # Chinese button
        zh_btn = Button(
            text="🇨🇳 中文\n\n简体中文\nSimplified Chinese",
            font_size='24sp',
            size_hint_y=0.25,
            bold=True,
            background_color=(0.9, 0.3, 0.3, 1),  # Red for China
            font_name=self.chinese_font or 'Roboto'  # ✅ 添加中文字体
        )
        zh_btn.bind(on_press=lambda instance: self.select_language('zh'))
        self.add_widget(zh_btn)
        
        # English button
        en_btn = Button(
            text="🇺🇸 English\n\nEnglish Language\n英语",
            font_size='24sp',
            size_hint_y=0.25,
            bold=True,
            background_color=(0.3, 0.5, 0.9, 1),  # Blue for US/UK
            font_name=self.chinese_font or 'Roboto'  # ✅ 添加中文字体
        )
        en_btn.bind(on_press=lambda instance: self.select_language('en'))
        self.add_widget(en_btn)
    
    def select_language(self, lang_code):
        """
        Handle language selection.
        
        Args:
            lang_code: 'zh' or 'en'
        """
        print(f"[Language] User selected: {lang_code}")
        language_manager.set_language(lang_code)
        
        # Call callback
        if self.on_language_selected:
            self.on_language_selected(lang_code)