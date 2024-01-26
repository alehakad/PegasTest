import asyncio

from environs import Env
from aiogram import Bot, Dispatcher
from handlers import handlers

env = Env()
env.read_env()

bot_token = env("BOT_TOKEN")


# main function
async def main(test=True):
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(handlers.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
