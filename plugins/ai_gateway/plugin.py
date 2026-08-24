from aiogram.types import Message

from core.plugin import BasePlugin

from . import repository
from .triggers import process_message

class AIGateway(BasePlugin):

    name = "ai_gateway"
    version = "2.1.2"

    async def setup(self) -> None:
        await repository.ensure_table(
            self.db,
            self.plugin_id
            )

    async def enable(self) -> None:
        pass

    async def on_message(self, message: Message) -> None:
        await process_message(message, self.bot, self.db)