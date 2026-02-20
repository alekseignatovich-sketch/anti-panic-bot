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
logger = logging.getLogger(__name__)

async def main():
    # Инициализация бота
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Удаляем ВСЕ вебхуки перед запуском
    try:
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url:
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info(f"🧹 Удалён вебхук: {webhook_info.url}")
    except Exception as e:
        logger.warning(f"⚠️ Не удалось проверить вебхук: {e}")
    
    # Инициализация диспетчера
    dp = Dispatcher()
    
    # Подключение роутеров (ПОРЯДОК ВАЖЕН!)
    dp.include_router(start.router)
    dp.include_router(quiz.router)
    dp.include_router(emergency.router)
    dp.include_router(guide.router)
    
    logger.info("✅ Бот запущен! Напишите ему в Telegram: /start")
    
    # Запуск пуллинга
    try:
        await dp.start_polling(bot, drop_pending_updates=True)
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Ошибка бота: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "Event loop is closed" not in str(e):
            raise
