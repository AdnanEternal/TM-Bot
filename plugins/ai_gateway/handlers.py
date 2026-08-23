from aiogram.types import Message
from .ai_service import AIService

async def ai_replying(message: Message) -> None:
    ai_service= AIService()
    ai_response=await ai_service.ask(message.text)
    await message.reply(
        ai_response
    )

