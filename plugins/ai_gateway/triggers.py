from aiogram.filters import Command
from aiogram import Bot
from aiogram.types import Message

from . import handlers


async def process_message(message: Message, bot: Bot) -> None:

    if not message.text:
        return

    if "بوبی" in message.text:
        await handlers.ai_replying(message)
