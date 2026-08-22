from core.plugin import BasePlugin


class Pong(BasePlugin):

    name = "Ping-Pong!"
    version = "0.1"

    def __init__(self, bot):
        super().__init__(bot)

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
        await message.reply(str(message.text))
    