from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import BotCommand


class CommandManager:

    def __init__(self):
        self.router = Router(
            name="commands"
        )

        self._commands: dict[str, object] = {}

    def register(
        self,
        *,
        name: str,
        handler,
        aliases: list[str] | None = None,
    ) -> None:

        names = [name]

        if aliases:
            names.extend(aliases)

        for command_name in names:

            if command_name in self._commands:
                raise ValueError(
                    f"Command '{command_name}' "
                    f"is already registered."
                )

            self.router.message.register(
                handler,
                Command(command_name),
            )

            self._commands[command_name] = handler


    async def sync_commands(self, bot: Bot) ->None:
        commands = [
            BotCommand(
                command=name,
                description=name,
            )
            for name in self._commands
        ]
        await bot.set_my_commands(commands)

    def has(self, name: str) -> bool:
        return name in self._commands

    def get(self, name: str):
        return self._commands.get(name)

    def all(self) -> dict[str, object]:
        return dict(self._commands)