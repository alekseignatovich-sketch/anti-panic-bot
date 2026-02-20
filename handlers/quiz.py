from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

router = Router()
logger = logging.getLogger(__name__)

# Хранилище данных
user_quiz_data = {}

class PanicQuiz(StatesGroup):
    symptoms = State()
    triggers = State()

@router.message(F.text.in_(['📝 Пройти квиз']))
async def start_quiz(message: Message, state: FSMContext):
    logger.info(f"📝 Квиз запущен. User: {message.from_user.id}")
    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💓 Сердцебиение"), KeyboardButton(text="🌬️ Удушье")],
            [KeyboardButton(text="🌀 Головокружение"), KeyboardButton(text="🧊 Озноб")],
            [KeyboardButton(text="➡️ Далее")]
        ],
        resize_keyboard=True
    )
    await state.set_state(PanicQuiz.symptoms)
    await message.answer("❓ Какие симптомы чаще всего?", reply_markup=kb)

@router.message(PanicQuiz.symptoms)
async def process_symptoms(message: Message, state: FSMContext):
    logger.info(f"💓 Симптом обработан: {message.text}. User: {message.from_user.id}")
    
    if message.text == "➡️ Далее":
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👥 Толпа"), KeyboardButton(text="💼 Работа")],
                [KeyboardButton(text="🏥 Здоровье"), KeyboardButton(text="🏠 Дома")],
                [KeyboardButton(text="✅ Готово")]
            ],
            resize_keyboard=True
        )
        await state.set_state(PanicQuiz.triggers)
        await message.answer("❓ Что запускает тревогу?", reply_markup=kb)
    else:
        user_id = message.from_user.id
        if user_id not in user_quiz_data:
            user_quiz_data[user_id] = {'symptoms': []}
        if message.text not in user_quiz_data[user_id]['symptoms']:
            user_quiz_data[user_id]['symptoms'].append(message.text)
        await message.answer("✅ Записал. Ещё или 'Далее'?")

@router.message(PanicQuiz.triggers)
async def process_triggers(message: Message, state: FSMContext):
    logger.info(f"🎯 Триггер обработан: {message.text}. User: {message.from_user.id}")
    
    if message.text != "✅ Готово":
        user_id = message.from_user.id
        if user_id not in user_quiz_data:
            user_quiz_data[user_id] = {}
        user_quiz_data[user_id]['triggers'] = message.text
    
    await state.clear()
    await message.answer(
        "✅ Квиз завершён!\n\n"
        "Теперь нажмите '📚 Мой гайд', чтобы получить "
        "персонализированный план самопомощи.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📚 Мой гайд")]],
            resize_keyboard=True
        )
    )
