from core.plugin import BasePlugin


class AIGateway(BasePlugin):

    name = "ai_gateway"
    version = "0.1"

    def setup(self) -> None:
        pass

    async def on_message(self, message) -> None:

        if not message.text:
            return

        if "بوبی" not in message.text:
            return

        await message.reply(
            "کسی منو صدا زد؟"
        )