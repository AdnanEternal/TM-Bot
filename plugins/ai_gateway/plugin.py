from aiogram.types import Message

from core.plugin import BasePlugin

from . import repository
from .triggers import process_message

class AIGateway(BasePlugin):

    name = "ai_gateway"
    version = "2.1.0"

    def setup(self) -> None:
        pass

    async def enable(self) -> None:
        await repository.ensure_table(self.db)
        await super().enable()

    async def on_message(self, message: Message) -> None:
        await process_message(message, self.bot, self.db)