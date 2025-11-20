from dotenv import load_dotenv
import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, BaseFilter

load_dotenv()

dp = Dispatcher()
bot = Bot(token=os.getenv("BOT_TOKEN"))

owner_id = int(os.getenv("OWNER_ID"))

class IsOwner(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id == owner_id

async def main():
    @dp.message(Command('start'), IsOwner())
    async def welcome(message: types.Message):
        await message.answer("Hello!")
    
    @dp.message(~IsOwner())
    async def unauthorized(message: types.Message):
        await message.answer("You are not the owner!")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())