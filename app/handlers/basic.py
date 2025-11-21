from aiogram import types
from aiogram.filters import Command

from app.filters.owner import IsOwner

def register_basic_handlers(dp):
    @dp.message(Command("start"), IsOwner())
    async def welcome(message: types.Message):
        await message.answer("Hello!")

    @dp.message(~IsOwner())
    async def unauthorized(message: types.Message):
        await message.answer("You are not the owner!")
