from abc import ABC, abstractmethod

from aiogram import Bot


class BasePlugin(ABC):

    name: str = "unknown"
    version: str = "1.0.0"
    description: str = "بدون شرح"
    

    def __init__(self, bot: Bot):
        self.bot = bot
        self.enabled = False

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError

    async def enable(self) -> None:
        self.enabled = True

    async def disable(self) -> None:
        self.enabled = False