from core.plugin import BasePlugin


class Pong(BasePlugin):

    name = "ping_pong"
    version = "0.1"

    def setup(self) -> None:
        pass

    async def on_message(self, message) -> None:

        print(5)