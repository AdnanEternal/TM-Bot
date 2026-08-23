from aiogram.types import Message

# from .triggers import is_ai_trigger

def is_ai_trigger(text: str) -> bool:
    return "بوبی" in text

async def on_message(message: Message) -> None:

    if not message.text:
        return

    if not is_ai_trigger(message.text):
        return

    await message.reply(
        "کسی منو صدا زد؟"
    )