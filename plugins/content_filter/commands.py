from aiogram.types import Message




def register(command_manager, plugin) -> None:

    command_manager.register(
        name="ping",
        handler=_bind(_pong,plugin),
    )

def _bind(func, plugin):
    async def handler(message: Message) -> None:
        await func(message, plugin)
    return handler

async def _pong(message: Message,plugin):
    await message.reply(text="pong")
