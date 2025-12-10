import asyncio
import os
from aiogram import Bot
from aiogram.filters import Command

from app.filters.owner import IsOwner
from app.services.clock import Clock
from app.graph.graph_24hr import graph_cpu_load
from app.database.readb import read_latest_24hr
from aiogram.types import FSInputFile

owner_id = int(os.getenv("OWNER_ID"))

async def send_report_24hr(bot: Bot):
    while True:
        print("Waiting for 24 hr clock")
        await Clock.daily_event.wait()
        Clock.daily_event.clear()

        latest = await read_latest_24hr()
        graph_cpu_load(latest)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_path = os.path.join(base_dir, 'graph', 'cpu_load.png')

        if not os.path.exists(img_path):
            await bot.send_message(chat_id=owner_id, text=f"Error: Graph file not found at {img_path}")
            return

        img = FSInputFile(img_path)
        await bot.send_photo(chat_id=owner_id, photo=img, caption="Graph over the last 24 hrs")

        #await bot.send_message(chat_id=owner_id, text="24-hour report triggered!")