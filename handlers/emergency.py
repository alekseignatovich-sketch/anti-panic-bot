from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import HOTLINES

router = Router()

def get_emergency_keyboard():
    """Клавиатура экстренной помощи"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📞 Горячие линии", callback_data="hotlines")],
        [InlineKeyboardButton(text="🎵 Аудио: Дыхание 4-7-8", callback_data="audio_breathing")],
        [InlineKeyboardButton(text="🧘 Техника 5-4-3-2-1", callback_data="technique_54321")],
        [InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="back_to_menu")]
    ])
    return kb

def get_54321_technique():
    """Техника заземления 5-4-3-2-1"""
    return (
        "🧘 <b>Техника заземления 5-4-3-2-1</b>\n\n"
        "<b>5</b> — Назовите 5 вещей, которые вы <b>видите</b> вокруг себя.\n"
        "Пример: стол, лампа, окно, книга, телефон.\n\n"
        "<b>4</b> — Назовите 4 вещи, которые вы можете <b>потрогать</b>.\n"
        "Пример: ткань одежды, стул, волосы, стол.\n\n"
        "<b>3</b> — Назовите 3 вещи, которые вы можете <b>услышать</b>.\n"
        "Пример: тиканье часов, шум за окном, своё дыхание.\n\n"
        "<b>2</b> — Назовите 2 вещи, которые вы можете <b>понюхать</b>.\n"
        "Пример: кофе, духи, свежий воздух.\n\n"
        "<b>1</b> — Назовите 1 вещь, которую вы можете <b>попробовать</b>.\n"
        "Пример: воду, жвачку, мятную конфету.\n\n"
        "💡 Эта техника помогает вернуть фокус в настоящее и снизить тревогу."
    )

@router.message(F.text.in_(['🆘 Мне плохо сейчас', '🆘 I feel bad now']))
async def emergency_help(message: Message):
    """Обработчик кнопки экстренной помощи"""
    await message.answer(
        "🆘 <b>Скорая помощь</b>\n\n"
        "Вы не одни. Вот несколько инструментов, которые могут помочь прямо сейчас:\n\n"
        "👇 Выберите то, что вам ближе:",
        reply_markup=get_emergency_keyboard()
    )

@router.callback_query(F.data == "technique_54321")
async def send_54321(callback):
    """Отправка техники 5-4-3-2-1"""
    await callback.message.answer(get_54321_technique())
    await callback.answer()

@router.callback_query(F.data == "hotlines")
async def send_hotlines(callback):
    """Отправка горячих линий"""
    hotlines_text = "📞 <b>Горячие линии поддержки:</b>\n\n" + "\n".join(HOTLINES['ru'])
    await callback.message.answer(hotlines_text)
    await callback.answer()
