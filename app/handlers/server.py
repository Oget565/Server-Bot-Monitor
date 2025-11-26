from app.database.readb import read_latest
from app.filters.owner import IsOwner
from aiogram import types
from aiogram.filters import Command

def server_stats_commands(dp):
    @dp.message(Command("now"), IsOwner())
    async def stats_now(message: types.Message):
        metrics = await read_latest()
        if metrics:
            await message.answer(
                f"{metrics}"
            )
        else:
            await message.answer("No metrics found.")
