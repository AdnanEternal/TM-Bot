from pathlib import Path
from typing import Optional

import aiosqlite

from config import config


class DatabaseManager:
    """
    لایه‌ی خام دیتابیس. فقط می‌خونه، می‌نویسه، جابه‌جا می‌کنه.
    هیچ ایده‌ای از schema یا داده‌ی پلاگین‌ها نداره — این مسئولیت خود پلاگین‌هاست.
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or config.get("DB_PATH", "data/bot.db")
        self.connection: Optional[aiosqlite.Connection] = None

    async def connect(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        self.connection = await aiosqlite.connect(self.db_path)
        self.connection.row_factory = aiosqlite.Row

        await self.connection.execute("PRAGMA journal_mode=WAL")
        await self.connection.execute("PRAGMA foreign_keys=ON")
        await self.connection.commit()

        print("✅ دیتابیس متصل شد.")

    async def close(self):
        if self.connection:
            await self.connection.close()
            print("🔌 اتصال دیتابیس بسته شد.")

    async def execute(self, query: str, params: tuple = ()):
        """برای INSERT / UPDATE / DELETE / CREATE TABLE. cursor رو برمی‌گردونه."""
        cursor = await self.connection.execute(query, params)
        await self.connection.commit()
        return cursor

    async def fetchone(self, query: str, params: tuple = ()):
        cursor = await self.connection.execute(query, params)
        row = await cursor.fetchone()
        await cursor.close()
        return row

    async def fetchall(self, query: str, params: tuple = ()):
        cursor = await self.connection.execute(query, params)
        rows = await cursor.fetchall()
        await cursor.close()
        return rows