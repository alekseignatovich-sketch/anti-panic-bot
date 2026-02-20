from aiogram import Router, F
from aiogram.types import Message
from groq import Groq
from config import GROQ_API_KEY
from prompts import get_guide_prompt
import asyncio

router = Router()

# Инициализация клиента Groq (с проверкой ключа)
if not GROQ_API_KEY or GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE":
    raise ValueError("❌ GROQ_API_KEY не установлен! Добавьте его в переменные окружения.")

client = Groq(api_key=GROQ_API_KEY)

# Импорт данных квиза (избегаем циклического импорта)
from handlers.quiz import user_quiz_data

@router.message(F.text.in_(['📚 Мой гайд', '📚 Получить гайд']))
async def generate_guide(message: Message):
    user_id = message.from_user.id
    
    if user_id not in user_quiz_data:
        await message.answer(
            "⚠️ Сначала пройдите квиз!\n"
            "Нажмите '📝 Пройти квиз'"
        )
        return
    
    await message.answer(
        "⏳ Генерирую ваш гайд...\n"
        "Groq работает за 2-3 секунды ⚡"
    )
    
    try:
        prompt = get_guide_prompt(user_quiz_data[user_id], lang='ru')
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Ты — помощник по самопомощи при тревоге. Отвечай кратко, с эмпатией."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
        )
        
        guide = response.choices[0].message.content
        await message.answer(guide)
        
    except Exception as e:
        error_msg = str(e)
        
        if "rate_limit" in error_msg.lower() or "429" in error_msg:
            await message.answer(
                "⚠️ Достигнут лимит запросов к ИИ (100/час).\n"
                "Попробуйте через 1 минуту или используйте статические техники ниже:\n\n"
                "🧘 <b>5-4-3-2-1</b>\n"
                "5 вещей видите → 4 трогаете → 3 слышите → 2 нюхаете → 1 пробуете"
            )
        else:
            await message.answer(
                f"❌ Ошибка: {error_msg[:200]}\n\n"
                "Но не волнуйтесь! Вот базовая техника:\n"
                "🌬️ <b>Дыхание 4-7-8</b>\n"
                "Вдох 4 сек → Задержка 7 сек → Выдох 8 сек → Повторить 4 раза"
            )
