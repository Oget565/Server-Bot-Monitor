from aiogram import types
from aiogram.filters import Command

from app.filters.owner import IsOwner

def register_basic_handlers(dp):
    @dp.message(Command("start"), IsOwner())
    async def welcome(message: types.Message):
        await message.answer(
            "Welcome! This is a bot to monitor your server.\n"
            "\n"
            "Quick start guide:\n"
            "/start - Starts the bot.\n"
            "/help - lists all of the available commands.\n"
        )

    @dp.message(Command("help"), IsOwner())
    async def list_commands(message: types.Message):
        await message.answer(
            "All of the available commands:\n"
            "/start - Starts the bot.\n"
            "/help - lists all of the available commands.\n"
            "/now - Show server's live stats.\n"
        )

    @dp.message(~IsOwner())
    async def unauthorized(message: types.Message):
        await message.answer(
            f"Sorry, you are not authorized to use this bot \n"
            f"\n"
            f"However, you can create your own bot using this link:\n" \
            f"https://github.com/Oget565/Server-Bot-Monitor\n"
        )
