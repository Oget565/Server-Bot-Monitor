import asyncio
import os
from aiogram import Bot, Dispatcher

from app.handlers.basic import register_basic_handlers
from app.services.metrics import wait_for_clock

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    register_basic_handlers(dp)

    metrics_task = asyncio.create_task(wait_for_clock())

    try:
        await dp.start_polling(bot)
    finally:
        metrics_task.cancel()
        try:
            await metrics_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(main())
