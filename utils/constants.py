# Copyright (c) 2025, TheSkyC
# SPDX-License-Identifier: Apache-2.0

import uuid
from utils.localization import _

APP_NAMESPACE_UUID = uuid.UUID('c2e02333-2f1d-48ba-bc8d-90d49da373af')
CONFIG_FILE = "localization_tool_config.json"
PROJECT_FILE_EXTENSION = ".owproj"
TM_FILE_EXCEL = "ow_translator_tm.xlsx"
EXPANSION_DATA_DIR = "expansion_data"
MAX_UNDO_HISTORY = 30
DEFAULT_API_URL = "https://api.deepseek.com/chat/completions"
APP_VERSION = "1.1.6"
PROMPT_PRESET_EXTENSION = ".owprompt"
EXTRACTION_PATTERN_PRESET_EXTENSION = ".owextract"

STRUCTURAL = "Structural Content"
STATIC = "Static Instruction"
DYNAMIC = "Dynamic Instruction"

DEFAULT_PROMPT_STRUCTURE = [
    {
        "id": str(uuid.uuid4()), "type": STRUCTURAL, "enabled": True,
        "content": "你是一个专业的游戏文本翻译器，负责将《守望先锋》自定义模式的界面UI文本和描述翻译成[Target Language]。\n请严格遵循以下要求："
    },
    {
        "id": str(uuid.uuid4()), "type": STATIC, "enabled": True,
        "content": "将以下文本翻译成[Target Language]语言。"
    },
    {
        "id": str(uuid.uuid4()), "type": DYNAMIC, "enabled": True,
        "content": "请遵循以下针对此项目的特定翻译指示：\n[Global Instructions]\n[Project Instructions]"
    },
    {
        "id": str(uuid.uuid4()), "type": STATIC, "enabled": True,
        "content": "如果原来的语言与目标语言一样，则不需要作改动。"
    },
    {
        "id": str(uuid.uuid4()), "type": STATIC, "enabled": True,
        "content": "所有符号必须保留。比如'\\n'，'\\r'，'任何空格'，'()'，'[]'，以及'.。?/\\'等等必须保留原样，无需翻译。同时，原来没有的符号也不要乱添加。"
    },
    {
        "id": str(uuid.uuid4()), "type": DYNAMIC, "enabled": True,
        "content": "请参考以下未翻译的原文上下文信息，以确保术语和风格的一致性（如果上下文与当前文本相关）：\n[Untranslated Context]"
    },
    {
        "id": str(uuid.uuid4()), "type": DYNAMIC, "enabled": True,
        "content": "请参考以下已翻译的译文上下文信息，以确保术语和风格的一致性（如果上下文与当前文本相关）：\n[Translated Context]"
    },
    {
        "id": str(uuid.uuid4()), "type": STATIC, "enabled": True,
        "content": "翻译结果应准确、简洁，并符合《守望先锋》的游戏内语言风格。"
    },
    {
        "id": str(uuid.uuid4()), "type": STRUCTURAL, "enabled": True,
        "content": "**重要：你的回答[必须且仅能包含翻译后的文本内容]，不要添加任何额外的解释、说明。**"
    }
]

DEFAULT_EXTRACTION_PATTERNS = [
    {
        "id": str(uuid.uuid4()), "name": "Custom String (EN/CN)", "enabled": True,
        "left_delimiter": r'(?:自定义字符串|Custom String)\s*\(\s*"',
        "right_delimiter": r'"',
        "string_type": "Custom String"
    },
    {
        "id": str(uuid.uuid4()), "name": "Description (EN/CN)", "enabled": True,
        "left_delimiter": r'(?:Description|描述)\s*:\s*"',
        "right_delimiter": r'"',
        "string_type": "Description"
    },
    {
        "id": str(uuid.uuid4()), "name": "Mode Name (EN/CN)", "enabled": True,
        "left_delimiter": r'(?:Mode Name|模式名称)\s*:\s*"',
        "right_delimiter": r'"',
        "string_type": "Mode Name"
    }
]

DEFAULT_KEYBINDINGS = {
    'open_code_file': 'Ctrl+O',
    'open_project': 'Ctrl+Shift+O',
    'save_current_file': 'Ctrl+S',
    'save_code_file': 'Ctrl+Shift+S',
    'undo': 'Ctrl+Z',
    'redo': 'Ctrl+Y',
    'find_replace': 'Ctrl+Shift+F',
    'copy_original': 'Ctrl+Shift+C',
    'paste_translation': 'Ctrl+Shift+V',
    'ai_translate_selected': 'Ctrl+T',
    'toggle_reviewed': 'Ctrl+R',
    'toggle_ignored': 'Ctrl+I',
    'apply_and_next': 'Ctrl+Return',
    'refresh_sort': 'F5',
}

SUPPORTED_LANGUAGES = {
    "Afrikaans": "af",
    "Amharic": "am",
    "Aragonese": "an",
    "Arabic": "ar",
    "Assamese": "as",
    "Azerbaijani": "az",
    "Belarusian": "be",
    "Bulgarian": "bg",
    "Bengali": "bn",
    "Breton": "br",
    "Catalan": "ca",
    "Czech": "cs",
    "Welsh": "cy",
    "Danish": "da",
    "Deutsch": "de",
    "Dzongkha": "dz",
    "Greek": "el",
    "English": "en",
    "Esperanto": "eo",
    "Español": "es",
    "Estonian": "et",
    "Basque": "eu",
    "Persian": "fa",
    "Finnish": "fi",
    "Français": "fr",
    "Western Frisian": "fy",
    "Irish": "ga",
    "Scottish Gaelic": "gd",
    "Galician": "gl",
    "Gujarati": "gu",
    "Hausa": "ha",
    "Hebrew": "he",
    "Hindi": "hi",
    "Croatian": "hr",
    "Hungarian": "hu",
    "Armenian": "hy",
    "Indonesian": "id",
    "Igbo": "ig",
    "Icelandic": "is",
    "Italiano": "it",
    "日本語": "ja",
    "Georgian": "ka",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kannada": "kn",
    "한국어": "ko",
    "Kurdish": "ku",
    "Kyrgyz": "ky",
    "Limburgish": "li",
    "Lithuanian": "lt",
    "Latvian": "lv",
    "Malagasy": "mg",
    "Macedonian": "mk",
    "Malayalam": "ml",
    "Mongolian": "mn",
    "Marathi": "mr",
    "Malay": "ms",
    "Maltese": "mt",
    "Burmese": "my",
    "Norwegian Bokmål": "nb",
    "Nepali": "ne",
    "Dutch": "nl",
    "Norwegian Nynorsk": "nn",
    "Norwegian": "no",
    "Occitan": "oc",
    "Oriya": "or",
    "Punjabi": "pa",
    "Polish": "pl",
    "Pashto": "ps",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Русский": "ru",
    "Kinyarwanda": "rw",
    "Northern Sami": "se",
    "Serbo-Croatian": "sh",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Albanian": "sq",
    "Serbian": "sr",
    "Swedish": "sv",
    "Tamil": "ta",
    "Telugu": "te",
    "Tajik": "tg",
    "Thai": "th",
    "Turkmen": "tk",
    "Turkish": "tr",
    "Tatar": "tt",
    "Uyghur": "ug",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Walloon": "wa",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "简体中文": "zh",
    "繁體中文": "zh_TW",
    "Zulu": "zu",
}