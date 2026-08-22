from aiogram import Bot

from core.plugin import BasePlugin

from .handlers import filter_message


class ContentFilterPlugin(BasePlugin):

    name = "content_filter"
    version = "1.0.0"

    def __init__(self, bot: Bot):
        super().__init__(bot)

        self.filtered_words: set[str] = {
            "فاک",
            "fuck",
        }

    def setup(self) -> None:

        self.router.message.register(
            self.on_message
        )

    async def on_message(
        self,
        message,
    ) -> None:

        if not self.enabled:
            return

        await filter_message(
            self,
            message,
        )