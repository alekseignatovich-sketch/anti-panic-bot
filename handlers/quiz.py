from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

# FSM состояния для квиза
class PanicQuiz(StatesGroup):
    waiting_for_symptoms = State()
    waiting_for_triggers = State()
    waiting_for_helpful = State()
    waiting_for_context = State()
    waiting_for_intensity = State()

# Хранилище ответов (в реальном проекте — база данных)
user_quiz_data = {}

def get_symptoms_keyboard(lang='ru'):
    """Клавиатура симптомов"""
    symptoms = {
        'ru': [
            ["💓 Сердцебиение", "🌬️ Удушье/не хватает воздуха"],
            ["🌀 Головокружение", "🧊 Озноб/потливость"],
            ["👻 Дереализация", "💥 Боль в груди"],
            ["➡️ Далее"]
        ]
    }
    
    kb = symptoms.get(lang, symptoms['ru'])
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t)] for row in kb for t in row], resize_keyboard=True)

@router.message(F.text.in_(['📝 Пройти квиз (персонализация)', '📝 Take Quiz (personalization)']))
async def start_quiz(message: Message, state: FSMContext):
    """Начало квиза"""
    lang = 'ru'  # В реальном проекте берём из user_languages
    
    await state.set_state(PanicQuiz.waiting_for_symptoms)
    
    await message.answer(
        "📋 <b>Шаг 1 из 5</b>\n\n"
        "Какие физические симптомы вы чаще всего ощущаете во время тревоги?\n"
        "(Выберите один или несколько)",
        reply_markup=get_symptoms_keyboard(lang)
    )

@router.message(PanicQuiz.waiting_for_symptoms)
async def process_symptoms(message: Message, state: FSMContext):
    """Обработка симптомов"""
    if message.text == "➡️ Далее":
        await state.set_state(PanicQuiz.waiting_for_triggers)
        
        triggers_kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👥 Толпа/люди")],
                [KeyboardButton(text="💼 Работа/дедлайны")],
                [KeyboardButton(text="🏥 Здоровье/врачи")],
                [KeyboardButton(text="🏠 Одиночество")],
                [KeyboardButton(text="➡️ Далее")]
            ],
            resize_keyboard=True
        )
        
        await message.answer(
            "📋 <b>Шаг 2 из 5</b>\n\n"
            "Что чаще всего запускает тревожное состояние?",
            reply_markup=triggers_kb
        )
    else:
        # Сохраняем симптом
        user_id = message.from_user.id
        if user_id not in user_quiz_data:
            user_quiz_data[user_id] = {'symptoms': []}
        
        user_quiz_data[user_id]['symptoms'].append(message.text)
        await message.answer("✅ Записал! Выберите ещё или нажмите 'Далее'")
