import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import Config, load_config
from handlers.users import user_router

logger = logging.getLogger(__name__)

async def main():

    
    logger.info("Starting bot...")
    
    config: Config = load_config()

    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format,
    )

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    
    logger.info("Including routers...")
    dp.include_router(user_router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(e)

asyncio.run(main())