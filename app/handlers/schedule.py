import asyncio
import os
from aiogram import Bot
from aiogram.filters import Command

from app.filters.owner import IsOwner
from app.services.clock import Clock
from app.graph.graph_24hr import graph_cpu_load
from app.database.readb import read_latest_24hr

owner_id = int(os.getenv("OWNER_ID"))

async def send_report_24hr(bot: Bot):
    while True:
        print("Waiting for 24 hr clock")
        await Clock.daily_event.wait()
        Clock.daily_event.clear()
        # cpu_load_graph = graph_cpu_load(read_latest_24hr())
        await bot.send_message(chat_id=owner_id, text="24-hour report triggered!")