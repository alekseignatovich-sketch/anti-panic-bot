from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from config import SUPPORTED_LANGUAGES, DISCLAIMER, HOTLINES

router = Router()
user_languages = {}

def get_main_keyboard(lang='ru'):
    texts = {
        'ru': {
            'quiz': '📝 Пройти квиз',
            'emergency': '🆘 Мне плохо сейчас',
            'guide': '📚 Получить гайд',
            'language': '🌐 Язык'
        }
    }
    t = texts[lang]
    kb = [
        [KeyboardButton(text=t['quiz'])],
        [KeyboardButton(text=t['emergency'])],
        [KeyboardButton(text=t['guide'])],
        [KeyboardButton(text=t['language'])]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@router.message(Command("start"))
async def cmd_start(message: Message):
    welcome = (
        "👋 Добро пожаловать в <b>Anti-Panic Bot</b>\n\n"
        "🧠 Инструменты для работы с тревогой и паническими атаками:\n"
        "• Персонализированный гайд под ваши симптомы\n"
        "• Техники «здесь и сейчас»\n"
        "• Горячие линии поддержки\n\n"
        f"{DISCLAIMER['ru']}\n\n"
        "<b>Выберите язык:</b>"
    )
    
    lang_kb = [[KeyboardButton(text=v)] for v in SUPPORTED_LANGUAGES.values()]
    await message.answer(
        welcome,
        reply_markup=ReplyKeyboardMarkup(keyboard=lang_kb, resize_keyboard=True)
    )

@router.message(F.text.in_(SUPPORTED_LANGUAGES.values()))
async def language_selected(message: Message):
    lang_code = next((k for k, v in SUPPORTED_LANGUAGES.items() if v == message.text), 'ru')
    user_languages[message.from_user.id] = lang_code
    
    await message.answer(
        f"✅ Язык: {message.text}\n\n"
        "Теперь выберите действие:",
        reply_markup=get_main_keyboard(lang_code)
    )
