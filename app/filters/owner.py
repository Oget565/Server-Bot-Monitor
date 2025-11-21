from aiogram.filters import BaseFilter
from aiogram import types
import os

owner_id = int(os.getenv("OWNER_ID"))

class IsOwner(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id == owner_id
