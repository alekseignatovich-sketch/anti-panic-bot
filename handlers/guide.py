from aiogram import Router, F
from aiogram.types import Message
from groq import Groq
from config import GROQ_API_KEY
from prompts import get_guide_prompt
import asyncio
import logging

router = Router()
logger = logging.getLogger(__name__)

# Инициализация клиента Groq (с проверкой ключа)
if not GROQ_API_KEY or GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE":
    raise ValueError("❌ GROQ_API_KEY не установлен! Добавьте его в переменные окружения.")

client = Groq(api_key=GROQ_API_KEY)

# Импорт данных квиза
from handlers.quiz import user_quiz_data

@router.message(F.text == '📚 Мой персональный гайд')
async def generate_guide(message: Message):
    user_id = message.from_user.id
    
    logger.info(f"📚 Запрос гайда. User: {user_id}")
    
    if user_id not in user_quiz_data or not user_quiz_data[user_id]:
        await message.answer(
            "⚠️ Сначала настройте бот под себя!\n"
            "Нажмите '🎯 Настроить под меня'"
        )
        return
    
    await message.answer(
        "⏳ <b>Генерирую ваш персонализированный гайд...</b>\n\n"
        "Groq работает быстро — обычно 2-3 секунды ⚡"
    )
    
    try:
        prompt = get_guide_prompt(user_quiz_data[user_id], lang='ru')
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Ты — помощник по самопомощи при тревоге. Отвечай кратко, с эмпатией, без медицинских диагнозов."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.7
            )
        )
        
        guide = response.choices[0].message.content
        
        # Отправляем гайд
        await message.answer(guide)
        
        await message.answer(
            "✅ <b>Ваш персонализированный гайд готов!</b>\n\n"
            "💡 <i>Совет:</i> Сохраните этот гайд скриншотом или перепишите ключевые моменты.\n"
            "Перечитывайте его в спокойном состоянии — это укрепляет нейронные связи.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="🆘 Мне плохо сейчас")],
                    [KeyboardButton(text="🎯 Настроить заново")]
                ],
                resize_keyboard=True
            )
        )
        
    except Exception as e:
        error_msg = str(e)
        
        logger.error(f"❌ Ошибка генерации гайда: {error_msg}")
        
        if "rate_limit" in error_msg.lower() or "429" in error_msg:
            await message.answer(
                "⚠️ <b>Достигнут лимит запросов к ИИ</b> (100/час).\n"
                "Попробуйте через 1 минуту или используйте бесплатные техники ниже:\n\n"
                "🧘 <b>Техника 5-4-3-2-1:</b>\n"
                "<b>5</b> вещей видите → <b>4</b> трогаете → <b>3</b> слышите → "
                "<b>2</b> нюхаете → <b>1</b> пробуете",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="🆘 Мне плохо сейчас")],
                        [KeyboardButton(text="🎯 Настроить заново")]
                    ],
                    resize_keyboard=True
                )
            )
        else:
            await message.answer(
                f"❌ <b>Ошибка:</b> {error_msg[:200]}\n\n"
                "Но не волнуйтесь! Вот базовая техника:\n\n"
                "🌬️ <b>Дыхание 4-7-8</b>\n"
                "Вдох 4 сек → Задержка 7 сек → Выдох 8 сек → Повторить 4 раза",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="🆘 Мне плохо сейчас")],
                        [KeyboardButton(text="🎯 Настроить заново")]
                    ],
                    resize_keyboard=True
                )
            )
