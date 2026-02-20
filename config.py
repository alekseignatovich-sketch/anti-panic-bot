import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')  # Groq вместо OpenAI

SUPPORTED_LANGUAGES = {
    'ru': '🇷🇺 Русский',
    'en': '🇬🇧 English',
    'by': '🇧🇾 Беларуская',
    'ua': '🇺🇦 Українська',
    'kz': '🇰🇿 Қазақ'
}

DISCLAIMER = {
    'ru': (
        "⚠️ ВАЖНО: Это информационный продукт для самопомощи. "
        "Не является заменой врачу. При острых симптомах обратитесь к специалисту."
    )
}

HOTLINES = {
    'ru': [
        "🇧🇾 Беларусь: 8-801-100-10-10 (телефон доверия)",
        "🇷🇺 Россия: 8-800-2000-122",
        "🌍 Международная линия: https://findahelpline.com"
    ]
}
