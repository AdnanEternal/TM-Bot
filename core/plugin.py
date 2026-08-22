from abc import ABC, abstractmethod

from aiogram import Bot, Router


class BasePlugin(ABC):

    name: str = "unknown"
    version: str = "1.0.0"

    def __init__(self, bot: Bot):
        self.bot = bot
        self.router = Router(name=self.name)

        self.enabled = False

    @abstractmethod
    def setup(self) -> None:
        """
        ثبت handlerها، commandها و تنظیمات پلاگین.
        """
        raise NotImplementedError

    async def enable(self) -> None:
        self.enabled = True

    async def disable(self) -> None:
        self.enabled = False