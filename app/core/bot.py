import asyncio
import os
from aiogram import Bot, Dispatcher

from app.handlers.basic import register_basic_handlers

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    register_basic_handlers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
