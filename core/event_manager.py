from aiogram.types import Message


class EventManager:

    def __init__(self, plugins):
        self.plugins = plugins

    async def handle_message(self, message: Message) -> None:

        for plugin in self.plugins:

            if not plugin.enabled:
                continue

            handler = getattr(
                plugin,
                "on_message",
                None,
            )

            if handler is None:
                continue

            try:
                await handler(message)

            except Exception as exc:
                print(
                    f"[{plugin.name}] "
                    f"message handler error: {exc}"
                )