import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tg_bot.config import load_config

from tg_bot.handlers.start import register_start_admin
from tg_bot.services.setting_commands import set_defoult_commands
logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    pass


def register_all_filters(dp):
    pass


def register_all_handlers(dp):
    register_start_admin(dp)


async def set_commands(bot: Bot):
    await set_defoult_commands(bot)


async def main():
    logging.basicConfig(
        level=logging.INFO, format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )

    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")

    # storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage
    # dp = Dispatcher(bot, storage=storage)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    await set_commands(bot)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
