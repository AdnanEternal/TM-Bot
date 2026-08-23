from aiogram import Bot

from core.plugin import BasePlugin

from .handlers import filter_message
from aiogram.dispatcher.event.bases import SkipHandler

class ContentFilterPlugin(BasePlugin):

    name = "content_filter"
    version = "0.1"

    def setup(self) -> None:
        pass

    async def on_message(self, message) -> None:

        if not message.text:
            return

        if "فاک" in message.text:
            await message.delete()