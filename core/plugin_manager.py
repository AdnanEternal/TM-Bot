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

    def discover(
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

            self._load_plugin(plugin_dir.name)

    def _load_plugin(self, plugin_name: str) -> None:

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

        plugin = plugin_class(bot=self.bot, db=self.db)
        plugin.setup()

        self.plugins[plugin.name] = plugin

        self._load_commands(plugin_name, plugin)

        print(f"Loaded plugin: {plugin.name} v{plugin.version}")

    def _load_commands(self, plugin_name: str, plugin: BasePlugin) -> None:
        """
        اگه پلاگین یه commands.py با تابع register(command_manager, plugin)
        داشته باشه، اجراش می‌کنیم. اختیاریه — plugin.py هیچ خبری ازش نداره.
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
        self.dispatcher.include_router(self.command_manager.router)

    async def enable_all(self) -> None:
        for plugin in self.plugins.values():
            await plugin.enable()

    async def disable_all(self) -> None:
        for plugin in self.plugins.values():
            await plugin.disable()