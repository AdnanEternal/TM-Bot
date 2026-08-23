from aiogram.types import Message

from . import repository
from .ai_service import AIService


async def ai_replying(message: Message, db) -> None:

    active_model = await repository.get_active_model(db)

    if active_model is None:
        await message.reply(
            "هیچ مدلی تنظیم نشده. اول با /addmodel یه مدل اضافه کن."
        )
        return

    ai_service = AIService(dict(active_model))
    ai_response = await ai_service.ask(message.text)

    await message.reply(ai_response)