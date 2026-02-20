from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from config import SUPPORTED_LANGUAGES, DISCLAIMER

router = Router()

# Хранилище языков пользователей (в реальном проекте — база данных)
user_languages = {}

def get_main_keyboard(lang='ru'):
    """Основная клавиатура"""
    texts = {
        'ru': {
            'quiz': '📝 Пройти квиз (персонализация)',
            'emergency': '🆘 Мне плохо сейчас',
            'guide': '📚 Получить гайд',
            'language': '🌐 Сменить язык'
        },
        'en': {
            'quiz': '📝 Take Quiz (personalization)',
            'emergency': '🆘 I feel bad now',
            'guide': '📚 Get Guide',
            'language': '🌐 Change Language'
        }
    }
    
    kb = [
        [KeyboardButton(text=texts[lang]['quiz'])],
        [KeyboardButton(text=texts[lang]['emergency'])],
        [KeyboardButton(text=texts[lang]['guide'])],
        [KeyboardButton(text=texts[lang]['language'])]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    
    # Приветственное сообщение на русском (можно сделать автоопределение)
    welcome_text = (
        "👋 Добро пожаловать в <b>Anti-Panic Bot</b>!\n\n"
        "🧠 Это пространство, где вы можете:\n"
        "• Получить инструменты для работы с тревогой\n"
        "• Создать персональный план самопомощи\n"
        "• Найти поддержку в момент кризиса\n\n"
        f"{DISCLAIMER['ru']}\n\n"
        "Выберите язык ниже 👇"
    )
    
    # Клавиатура выбора языка
    lang_kb = [
        [KeyboardButton(text=SUPPORTED_LANGUAGES['ru'])],
        [KeyboardButton(text=SUPPORTED_LANGUAGES['en'])],
        [KeyboardButton(text=SUPPORTED_LANGUAGES['by'])],
        [KeyboardButton(text=SUPPORTED_LANGUAGES['ua'])],
        [KeyboardButton(text=SUPPORTED_LANGUAGES['kz'])]
    ]
    
    await message.answer(
        welcome_text,
        reply_markup=ReplyKeyboardMarkup(keyboard=lang_kb, resize_keyboard=True)
    )

@router.message(F.text.in_(SUPPORTED_LANGUAGES.values()))
async def language_selected(message: Message):
    """Обработчик выбора языка"""
    # Определяем код языка по тексту кнопки
    lang_code = None
    for code, text in SUPPORTED_LANGUAGES.items():
        if message.text == text:
            lang_code = code
            break
    
    if lang_code:
        user_languages[message.from_user.id] = lang_code
        
        # Приветствие на выбранном языке
        greetings = {
            'ru': "🇷🇺 Язык установлен: Русский",
            'en': "🇬🇧 Language set: English",
            'by': "🇧🇾 Мова ўстаноўлена: Беларуская",
            'ua': "🇺🇦 Мова встановлена: Українська",
            'kz': "🇰🇿 Тіл орнатылды: Қазақ"
        }
        
        await message.answer(
            f"✅ {greetings[lang_code]}\n\n"
            "Теперь вы можете использовать бота!",
            reply_markup=get_main_keyboard(lang_code)
        )
