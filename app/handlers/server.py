from app.database.readb import read_latest
from app.filters.owner import IsOwner
from aiogram import types
from aiogram.filters import Command
import datetime

def server_stats_commands(dp):
    @dp.message(Command("now"), IsOwner())
    async def stats_now(message: types.Message):
        metrics = await read_latest()
        time = datetime.datetime.fromtimestamp(metrics['timestamp'])

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
