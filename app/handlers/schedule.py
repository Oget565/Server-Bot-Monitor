import asyncio
import os
from aiogram import Bot
from aiogram.filters import Command

from app.filters.owner import IsOwner
from app.services.clock import Clock

owner_id = int(os.getenv("OWNER_ID"))

async def send_report_24hr(bot: Bot):
    while True:
        print("Waiting for 24 hr clock")
        await Clock.daily_event.wait()
        Clock.daily_event.clear()

        await bot.send_message(chat_id=owner_id, text="24-hour report triggered!")