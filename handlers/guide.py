from aiogram import Router, F
from aiogram.types import Message
from openai import AsyncOpenAI
from config import OPENAI_API_KEY
from prompts import get_guide_prompt
import asyncio

router = Router()

# Инициализация OpenAI клиента
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

@router.message(F.text.in_(['📚 Получить гайд', '📚 Get Guide']))
async def generate_guide(message: Message):
    """Генерация персонализированного гайда"""
    user_id = message.from_user.id
    
    # Проверяем, прошёл ли пользователь квиз
    from handlers.quiz import user_quiz_data
    
    if user_id not in user_quiz_data or not user_quiz_data[user_id]:
        await message.answer(
            "⚠️ Для персонализированного гайда нужно пройти квиз сначала.\n"
            "Нажмите '📝 Пройти квиз (персонализация)'"
        )
        return
    
    await message.answer("⏳ Генерирую ваш персонализированный гайд...\nЭто займёт 10-15 секунд.")
    
    try:
        # Получаем промпт
        prompt = get_guide_prompt(user_quiz_data[user_id], lang='ru')
        
        # Запрос к OpenAI
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты — помощник по самопомощи при тревоге."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        guide_text = response.choices[0].message.content
        
        # Отправляем гайд (разбиваем на части, если длинный)
        max_message_length = 4096
        for i in range(0, len(guide_text), max_message_length):
            await message.answer(guide_text[i:i + max_message_length])
        
        await message.answer(
            "✅ Ваш персонализированный гайд готов!\n"
            "Сохраните его или вернитесь сюда позже."
        )
        
    except Exception as e:
        await message.answer(
            f"❌ Произошла ошибка при генерации гайда: {str(e)}\n"
            "Попробуйте ещё раз или обратитесь к разработчику."
        )
