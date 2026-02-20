from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import HOTLINES

router = Router()

def get_emergency_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧘 5-4-3-2-1", callback_data="technique_54321")],
        [InlineKeyboardButton(text="🌬️ 4-7-8", callback_data="breathing_478")],
        [InlineKeyboardButton(text="📞 Линии", callback_data="hotlines")],
        [InlineKeyboardButton(text="🏠 Меню", callback_data="menu")]
    ])

def technique_54321():
    return (
        "🧘 <b>Техника 5-4-3-2-1</b>\n\n"
        "<b>5</b> — Вещи, которые <b>видите</b>\n"
        "<b>4</b> — Что можете <b>потрогать</b>\n"
        "<b>3</b> — Что <b>слышите</b>\n"
        "<b>2</b> — Что <b>нюхаете</b>\n"
        "<b>1</b> — Что <b>пробуете</b>\n\n"
        "Делайте медленно. Это возвращает в «здесь и сейчас»."
    )

def breathing_478():
    return (
        "🌬️ <b>Дыхание 4-7-8</b>\n\n"
        "1. Вдох носом — <b>4</b> сек\n"
        "2. Задержка — <b>7</b> сек\n"
        "3. Выдох ртом — <b>8</b> сек\n"
        "4. Повторить <b>4 раза</b>\n\n"
        "⚠️ Не больше 4 циклов при первом использовании."
    )

@router.message(F.text.in_(['🆘 Мне плохо', '🆘 Мне плохо сейчас']))
async def emergency(message: Message):
    await message.answer(
        "🆘 <b>Скорая помощь</b>\n\n"
        "Выберите технику:",
        reply_markup=get_emergency_kb()
    )

@router.callback_query(F.data == "technique_54321")
async def send_54321(callback):
    await callback.message.answer(technique_54321())
    await callback.answer()  # ⚠️ ОБЯЗАТЕЛЬНО подтверждаем коллбэк!

@router.callback_query(F.data == "breathing_478")
async def send_478(callback):
    await callback.message.answer(breathing_478())
    await callback.answer()  # ⚠️ ОБЯЗАТЕЛЬНО подтверждаем коллбэк!

@router.callback_query(F.data == "hotlines")
async def send_hotlines(callback):
    text = "📞 <b>Горячие линии:</b>\n\n" + "\n".join(HOTLINES['ru'])
    await callback.message.answer(text)
    await callback.answer()  # ⚠️ ОБЯЗАТЕЛЬНО подтверждаем коллбэк!

@router.callback_query(F.data == "menu")
async def back_to_menu(callback):
    from handlers.start import get_main_keyboard
    await callback.message.answer(
        "🏠 Вы в главном меню:",
        reply_markup=get_main_keyboard('ru')
    )
    await callback.answer()  # ⚠️ ОБЯЗАТЕЛЬНО подтверждаем коллбэк!
