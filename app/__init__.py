import logging
from os import environ
from typing import Tuple
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.utils.token import TokenValidationError
from aiogram.exceptions import TelegramNetworkError
from aiogram.client.default import DefaultBotProperties

from core import log
from core.config import TelegramConfig
from handlers import get_router

load_dotenv("./.env")
logger = logging.getLogger(__name__)
cfg = TelegramConfig()


def prepare_bot_dispatcher() -> Tuple[Bot, Dispatcher]:
    """Prepare web application.

    Create Telegram instances.
    """
    api_server = TelegramAPIServer.from_base(cfg.local_server_url,
                                             is_local=True)

    try:
        bot = Bot(token=environ['TELEGRAM_TOKEN'],
                  session=AiohttpSession(api=api_server),
                  default=DefaultBotProperties(parse_mode="HTML",
                                               protect_content=False))
    except TokenValidationError as e:
        logging.error("Указан нерабочий токен.")
        exit(1)
    except KeyError as e:
        logging.error("В файле env нет переменной TELEGRAM_TOKEN.")
        exit(1)
    except TelegramNetworkError as e:
        logging.error(e)
        exit(1)
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    router = get_router()
    dp.include_router(router)
    return bot, dp


async def on_startup(bot: Bot):
    """Setup app on startup."""
    log.setup()
    logger.warning("Starting bot with %s", cfg)


async def on_shutdown(bot: Bot):
    """Tear down app on shutdown."""
    await bot.session.close()
    logger.warning("Bot stopped.")
