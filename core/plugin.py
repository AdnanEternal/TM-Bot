from abc import ABC, abstractmethod
from typing import Optional

from aiogram import Bot

from core.database_manager import DatabaseManager


class BasePlugin(ABC):

    name: str = "unknown"
    version: str = "1.0.0"
    description: str = "بدون شرح"

    def __init__(
            self, 
            bot: Bot, 
            db: DatabaseManager
    ):
        
        self.bot = bot
        self.db = db
        self.plugin_id: Optional[int] = None
        self.enabled = False

    @abstractmethod
    async def setup(self) -> None:
        raise NotImplementedError

    async def enable(self) -> None:
        self.enabled = True

    async def disable(self) -> None:
        self.enabled = False