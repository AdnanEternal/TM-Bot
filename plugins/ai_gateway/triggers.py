from aiogram import Bot
from aiogram.types import Message

from . import handlers


async def process_message(message: Message, bot: Bot, db) -> None:

    if not message.text:
        return

    if "بوبی" in message.text:
        print(message.text)
        await handlers.ai_replying(message, db)