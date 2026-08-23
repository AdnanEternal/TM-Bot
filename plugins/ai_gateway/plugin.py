from aiogram.types import Message

from core.plugin import BasePlugin

from .triggers import process_message


class AIGateway(BasePlugin):

    name = "ai_gateway"
    version = "10.0"

    def setup(self) -> None:
        pass

    async def on_message(self, message: Message) -> None:
        await process_message(message,self.bot)