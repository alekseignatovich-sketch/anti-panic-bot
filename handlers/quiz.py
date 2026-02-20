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
    context = State()

@router.message(F.text == '🎯 Настроить под меня')
async def start_quiz(message: Message, state: FSMContext):
    logger.info(f"🎯 Опрос запущен. User: {message.from_user.id}")
    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💓 Сердцебиение"), KeyboardButton(text="🌬️ Удушье/не хватает воздуха")],
            [KeyboardButton(text="🌀 Головокружение"), KeyboardButton(text="🧊 Озноб/потливость")],
            [KeyboardButton(text="👻 Дереализация"), KeyboardButton(text="💥 Боль в груди")],
            [KeyboardButton(text="➡️ Пропустить")]
        ],
        resize_keyboard=True
    )
    await state.set_state(PanicQuiz.symptoms)
    await message.answer(
        "📋 <b>Шаг 1 из 3</b>\n\n"
        "Какие физические симптомы вы чаще всего ощущаете во время тревоги?\n"
        "<i>Выберите один или несколько:</i>",
        reply_markup=kb
    )

@router.message(PanicQuiz.symptoms)
async def process_symptoms(message: Message, state: FSMContext):
    logger.info(f"💓 Симптом: {message.text}. User: {message.from_user.id}")
    
    if message.text == "➡️ Пропустить":
        await state.update_data(symptoms=[])
    else:
        if message.from_user.id not in user_quiz_data:
            user_quiz_data[message.from_user.id] = {'symptoms': []}
        
        if message.text not in user_quiz_data[message.from_user.id]['symptoms']:
            user_quiz_data[message.from_user.id]['symptoms'].append(message.text)
        
        await message.answer("✅ Записал! Выберите ещё или нажмите '➡️ Пропустить'")
        return
    
    # Переход к следующему шагу
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👥 Толпа/люди")],
            [KeyboardButton(text="💼 Работа/дедлайны")],
            [KeyboardButton(text="🏥 Здоровье/врачи")],
            [KeyboardButton(text="🏠 Одиночество/дома")],
            [KeyboardButton(text="➡️ Пропустить")]
        ],
        resize_keyboard=True
    )
    await state.set_state(PanicQuiz.triggers)
    await message.answer(
        "📋 <b>Шаг 2 из 3</b>\n\n"
        "Что чаще всего запускает тревожное состояние?",
        reply_markup=kb
    )

@router.message(PanicQuiz.triggers)
async def process_triggers(message: Message, state: FSMContext):
    logger.info(f"🎯 Триггер: {message.text}. User: {message.from_user.id}")
    
    if message.text == "➡️ Пропустить":
        trigger = "не указан"
    else:
        trigger = message.text
    
    user_id = message.from_user.id
    if user_id not in user_quiz_data:
        user_quiz_data[user_id] = {}
    user_quiz_data[user_id]['triggers'] = trigger
    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏢 На работе")],
            [KeyboardButton(text="🏠 Дома")],
            [KeyboardButton(text="🚇 В транспорте")],
            [KeyboardButton(text="🛒 В магазине/публичных местах")],
            [KeyboardButton(text="➡️ Пропустить")]
        ],
        resize_keyboard=True
    )
    await state.set_state(PanicQuiz.context)
    await message.answer(
        "📋 <b>Шаг 3 из 3</b>\n\n"
        "Где чаще всего происходит?",
        reply_markup=kb
    )

@router.message(PanicQuiz.context)
async def process_context(message: Message, state: FSMContext):
    logger.info(f"📍 Контекст: {message.text}. User: {message.from_user.id}")
    
    if message.text == "➡️ Пропустить":
        context = "не указан"
    else:
        context = message.text
    
    user_id = message.from_user.id
    if user_id not in user_quiz_data:
        user_quiz_data[user_id] = {}
    user_quiz_data[user_id]['context'] = context
    
    await state.clear()
    
    # Финальное сообщение с кнопкой гайда
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Мой персональный гайд")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "✅ <b>Настройка завершена!</b>\n\n"
        "Теперь вы можете получить ваш персонализированный гайд "
        "для работы с тревогой.\n\n"
        "Нажмите кнопку ниже 👇",
        reply_markup=kb
    )
