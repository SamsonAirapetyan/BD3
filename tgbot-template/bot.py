import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tg_bot.config import load_config

from tg_bot.middlewares.Callback import Buttons

from tg_bot.handlers.start import register_start_admin
from tg_bot.handlers.Add_info import register_add_info
from tg_bot.handlers.add_work_repair import register_add_repair_work
from tg_bot.handlers.Add_Worker_info import register_add_info_worker
from tg_bot.handlers.function import register_function
from tg_bot.services.setting_commands import set_defoult_commands
from tg_bot.filters.Admin import IsAdmin
from tg_bot.models.Mariadb import Database

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.middleware.setup(Buttons())


def register_all_filters(dp):
    dp.filters_factory.bind(IsAdmin)


def register_all_handlers(dp):
    register_start_admin(dp)
    register_add_info(dp)
    register_add_info_worker(dp)
    register_add_repair_work(dp)
    register_function(dp)


async def set_commands(bot: Bot):
    await set_defoult_commands(bot)


async def main():
    logging.basicConfig(
        level=logging.INFO, format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )

    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")

    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    db = Database()
    await db.create()

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
        asyncio.get_event_loop().run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
