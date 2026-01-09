from aiogram.filters import BaseFilter
from aiogram import types
import os

owner_id_str = os.getenv("OWNER_ID")
if not owner_id_str:
    raise ValueError("OWNER_ID environment variable is not set")
owner_id = int(owner_id_str)

class IsOwner(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id == owner_id