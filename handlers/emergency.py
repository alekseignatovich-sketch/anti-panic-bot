from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import HOTLINES

router = Router()

def get_emergency_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧘 Техника 5-4-3-2-1", callback_data="technique_54321")],
        [InlineKeyboardButton(text="🌬️ Дыхание 4-7-8", callback_data="breathing_478")],
        [InlineKeyboardButton(text="📞 Горячие линии", callback_data="hotlines")],
        [InlineKeyboardButton(text="🏠 Меню", callback_data="menu")]
    ])

def technique_54321():
    return (
        "🧘 <b>Техника заземления 5-4-3-2-1</b>\n\n"
        "<b>5</b> — Назовите 5 вещей, которые <b>видите</b>\n"
        "<b>4</b> — 4 вещи, которые можете <b>потрогать</b>\n"
        "<b>3</b> — 3 вещи, которые <b>слышите</b>\n"
        "<b>2</b> — 2 вещи, которые <b>нюхаете</b>\n"
        "<b>1</b> — 1 вещь, которую <b>пробуете</b>\n\n"
        "💡 Делайте медленно, фокусируясь на ощущениях. "
        "Это возвращает мозг в «здесь и сейчас»."
    )

def breathing_478():
    return (
        "🌬️ <b>Дыхание 4-7-8</b>\n\n"
        "1. Выдохните полностью через рот\n"
        "2. Закройте рот, вдохните через нос на <b>4</b> счёта\n"
        "3. Задержите дыхание на <b>7</b> счётов\n"
        "4. Выдохните через рот на <b>8</b> счётов\n"
        "5. Повторите <b>4 раза</b>\n\n"
        "⚠️ Не делайте больше 4 циклов подряд при первом использовании."
    )

@router.message(F.text.in_(['🆘 Мне плохо сейчас']))
async def emergency(message: Message):
    await message.answer(
        "🆘 <b>Скорая помощь</b>\n\n"
        "Выберите технику, которая вам ближе:",
        reply_markup=get_emergency_kb()
    )

@router.callback_query(F.data == "technique_54321")
async def send_54321(callback):
    await callback.message.answer(technique_54321())
    await callback.answer()

@router.callback_query(F.data == "breathing_478")
async def send_478(callback):
    await callback.message.answer(breathing_478())
    await callback.answer()

@router.callback_query(F.data == "hotlines")
async def send_hotlines(callback):
    text = "📞 <b>Горячие линии:</b>\n\n" + "\n".join(HOTLINES['ru'])
    await callback.message.answer(text)
    await callback.answer()
