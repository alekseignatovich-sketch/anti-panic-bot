from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers.guide import user_quiz_data  # Импорт хранилища

router = Router()

class PanicQuiz(StatesGroup):
    symptoms = State()
    triggers = State()
    done = State()

@router.message(F.text.in_(['📝 Пройти квиз']))
async def start_quiz(message: Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💓 Сердцебиение"), KeyboardButton(text="🌬️ Удушье")],
            [KeyboardButton(text="🌀 Головокружение"), KeyboardButton(text="🧊 Озноб")],
            [KeyboardButton(text="➡️ Далее")]
        ],
        resize_keyboard=True
    )
    await state.set_state(PanicQuiz.symptoms)
    await message.answer("❓ Какие симптомы вы ощущаете чаще всего?", reply_markup=kb)

@router.message(PanicQuiz.symptoms)
async def process_symptoms(message: Message, state: FSMContext):
    if message.text == "➡️ Далее":
        await state.set_state(PanicQuiz.triggers)
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👥 Толпа"), KeyboardButton(text="💼 Работа")],
                [KeyboardButton(text="🏥 Здоровье"), KeyboardButton(text="🏠 Дома")],
                [KeyboardButton(text="✅ Готово")]
            ],
            resize_keyboard=True
        )
        await message.answer("❓ Что чаще всего запускает тревогу?", reply_markup=kb)
    else:
        user_id = message.from_user.id
        if user_id not in user_quiz_data:
            user_quiz_data[user_id] = {'symptoms': []}
        user_quiz_data[user_id]['symptoms'].append(message.text)
        await message.answer("✅ Записал. Выберите ещё или 'Далее'")

@router.message(PanicQuiz.triggers)
async def process_triggers(message: Message, state: FSMContext):
    if message.text == "✅ Готово":
        user_id = message.from_user.id
        if user_id not in user_quiz_data:
            user_quiz_data[user_id] = {}
        user_quiz_data[user_id]['triggers'] = 'не указаны'
        
        await state.clear()
        await message.answer(
            "✅ Квиз завершён!\n\n"
            "Теперь нажмите '📚 Получить гайд', чтобы сгенерировать "
            "персонализированный план самопомощи.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="📚 Получить гайд")]],
                resize_keyboard=True
            )
        )
    else:
        user_id = message.from_user.id
        if user_id not in user_quiz_data:
            user_quiz_data[user_id] = {}
        user_quiz_data[user_id]['triggers'] = message.text
        await message.answer("✅ Триггер записан. Нажмите 'Готово'")
