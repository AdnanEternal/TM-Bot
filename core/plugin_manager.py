import importlib
import inspect
from pathlib import Path

from aiogram import Bot, Dispatcher

from core.plugin import BasePlugin
from core.command_manager import CommandManager
from core.database_manager import DatabaseManager


class PluginManager:

    def __init__(
        self,
        bot: Bot,
        dispatcher: Dispatcher,
        db: DatabaseManager,
    ):
        self.bot = bot
        self.dispatcher = dispatcher
        self.db = db

        self.command_manager = CommandManager()

        self.plugins: dict[str, BasePlugin] = {}

    async def initialize(self) -> None:

        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS plugins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                version TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                enabled INTEGER NOT NULL DEFAULT 1
            )
            """
        )

    async def discover(
        self,
        plugins_directory: str = "plugins",
    ) -> None:

        base_path = Path(plugins_directory)

        for plugin_dir in sorted(base_path.iterdir()):

            if not plugin_dir.is_dir():
                continue

            if plugin_dir.name.startswith("_"):
                continue

            plugin_module = plugin_dir / "plugin.py"

            if not plugin_module.exists():
                continue

            await self._load_plugin(plugin_dir.name)

    async def _load_plugin(self, plugin_name: str) -> None:

        module_path = f"plugins.{plugin_name}.plugin"
        module = importlib.import_module(module_path)

        plugin_class = None

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, BasePlugin)
                and obj is not BasePlugin
                and obj.__module__ == module.__name__
            ):
                plugin_class = obj
                break

        if plugin_class is None:
            raise RuntimeError(f"No plugin class found in {module_path}")

        # اول خود Plugin را می‌سازیم تا name/version را داشته باشیم.
        plugin = plugin_class(
            bot=self.bot,
            db=self.db,
        )

        # ثبت پلاگین در جدول plugins
        await self._register_plugin(plugin)

        # بعد از ثبت، plugin_id در دسترس خود Plugin است.
        plugin.setup()

        self.plugins[plugin.name] = plugin

        self._load_commands(plugin_name, plugin)

        print(
            f"Loaded plugin: "
            f"{plugin.name} v{plugin.version} "
            f"(id={plugin.plugin_id})"
        )

    async def _register_plugin(self, plugin: BasePlugin) -> None:
        """
        Plugin را در جدول plugins ثبت یا بروزرسانی می‌کند
        و شناسه‌ی آن را داخل plugin.plugin_id قرار می‌دهد.
        """

        await self.db.execute(
            """
            INSERT INTO plugins (
                name,
                version,
                description,
                enabled
            )
            VALUES (?, ?, ?, 1)
            ON CONFLICT(name) DO UPDATE SET
                version = excluded.version,
                description = excluded.description
            """,
            (
                plugin.name,
                plugin.version,
                plugin.description,
            ),
        )

        row = await self.db.fetchone(
            """
            SELECT id
            FROM plugins
            WHERE name = ?
            """,
            (plugin.name,),
        )

        if row is None:
            raise RuntimeError(
                f"Failed to register plugin: {plugin.name}"
            )

        plugin.plugin_id = row["id"]

    def _load_commands(
        self,
        plugin_name: str,
        plugin: BasePlugin,
    ) -> None:
        """
        اگه پلاگین commands.py داشته باشه،
        تابع register آن را اجرا می‌کنیم.
        """

        module_path = f"plugins.{plugin_name}.commands"

        try:
            module = importlib.import_module(module_path)
        except ModuleNotFoundError:
            return

        register = getattr(module, "register", None)

        if register is None:
            return

        register(self.command_manager, plugin)

    def include_command_router(self) -> None:
        self.dispatcher.include_router(
            self.command_manager.router
        )

    async def enable_all(self) -> None:
        for plugin in self.plugins.values():
            await plugin.enable()

    async def disable_all(self) -> None:
        for plugin in self.plugins.values():
            await plugin.disable()