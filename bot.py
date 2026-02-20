import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers import start, quiz, emergency, guide

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    # Инициализация бота
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Инициализация диспетчера
    dp = Dispatcher()
    
    # Подключение роутеров (каждый только один раз)
    dp.include_router(start.router)
    dp.include_router(quiz.router)
    dp.include_router(emergency.router)
    dp.include_router(guide.router)
    
    # Удаляем вебхук и сбрасываем pending обновления
    await bot.delete_webhook(drop_pending_updates=True)
    
    logging.info("✅ Бот запущен! Напишите ему в Telegram: /start")
    
    # Запуск пуллинга
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logging.error(f"❌ Ошибка бота: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        # Игнорируем ошибку "Event loop is closed" на Windows
        if "Event loop is closed" not in str(e):
            raise
