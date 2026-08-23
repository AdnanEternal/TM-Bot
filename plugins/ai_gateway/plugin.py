from aiogram import Bot

from core.plugin import BasePlugin

from .handlers import on_message



class AIGateway(BasePlugin):
    name = "ai_gateway"
    version = "0.1"

    def __init__(self, bot: Bot):
        super().__init__(bot)

    def setup(self) -> None:

        self.router.message.register(
            on_message
        )