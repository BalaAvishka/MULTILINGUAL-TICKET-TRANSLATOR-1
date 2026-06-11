from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from deep_translator import GoogleTranslator

LANG_NAMES = {
    'hi': 'Hindi', 'ta': 'Tamil', 'te': 'Telugu', 'kn': 'Kannada',
    'ml': 'Malayalam', 'mr': 'Marathi', 'bn': 'Bengali', 'gu': 'Gujarati',
    'fr': 'French', 'de': 'German', 'es': 'Spanish', 'ar': 'Arabic',
    'zh-cn': 'Chinese', 'ja': 'Japanese', 'ko': 'Korean', 'pt': 'Portuguese',
    'en': 'English'
}

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except LangDetectException:
        return 'en'

def get_language_name(lang_code: str) -> str:
    return LANG_NAMES.get(lang_code, lang_code.upper())

def translate_to_english(text: str, source_lang: str) -> str:
    return GoogleTranslator(source=source_lang, target='en').translate(text)

def translate_from_english(text: str, target_lang: str) -> str:
    return GoogleTranslator(source='en', target=target_lang).translate(text)
