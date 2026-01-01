from aiogram import types
from aiogram.filters import Command
import asyncio
from app.filters.owner import IsOwner

def settings_commands(dp):
    @dp.message(Command("settings"), IsOwner())
    async def get_keyboard(message: types.Message):
        await message.answer("Settings are working")
