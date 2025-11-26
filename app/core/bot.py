import asyncio
import os
from aiogram import Bot, Dispatcher

from app.handlers.basic import register_basic_handlers
from app.handlers.schedule import send_report_24hr
from app.handlers.server import server_stats_commands
from app.services.metrics import wait_for_clock
from app.services.clock import Clock

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    register_basic_handlers(dp)
    server_stats_commands(dp)

    clock = Clock()
    clock_task = asyncio.create_task(clock.day_cycle_clock())
    report_task = asyncio.create_task(send_report_24hr(bot))
    metrics_task = asyncio.create_task(wait_for_clock())

    try:
        await dp.start_polling(bot)
    finally:
        clock_task.cancel()
        report_task.cancel()
        metrics_task.cancel()
        try:
            await report_task
        except asyncio.CancelledError:
            pass
        try:
            await metrics_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(main())
