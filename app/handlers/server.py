from curses.ascii import islower
import os
import pytz
from app.database.readb import read_latest
from app.filters.owner import IsOwner
from app.graph.graph_24hr import graph_cpu_load
from app.database.readb import read_latest_24hr
from aiogram import types, Bot
from aiogram.filters import Command
from aiogram.types import FSInputFile
import datetime

def server_stats_commands(dp):
    @dp.message(Command("now"), IsOwner())
    async def stats_now(message: types.Message):
        metrics = await read_latest()
        tz = pytz.timezone('America/New_York')
        time = datetime.datetime.fromtimestamp(metrics['timestamp'], tz=tz)

        if metrics:
            await message.answer(
                f"Stats as of {time}: \n"
                f"Total RAM - {metrics['mem_total']}GB\n"
                f"Used RAM - {metrics['mem_used']}GB ({metrics['mem_prcnt']}%)\n"
                f"CPU load - {metrics['cpu_prcnt']}%\n"
                f"CPU frequency - {metrics['cpu_freq']}GHz\n"
                f"CPU temperature - {metrics['cpu_temp']}C"
            )
        else:
            await message.answer("No metrics found.")

    @dp.message(Command("cpu_graph"), IsOwner())
    async def cpu_graph_img(message: types.Message):
        data = await read_latest_24hr()
        graph_cpu_load(data)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_path = os.path.join(base_dir, 'graph', 'cpu_load.png')

        if not os.path.exists(img_path):
            await message.answer(f"Error: Graph file not found at {img_path}")
            return

        img = FSInputFile(img_path)
        await message.answer_photo(photo=img, caption="Graph over the last 24 hrs")
