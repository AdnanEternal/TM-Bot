import importlib
import inspect
from pathlib import Path

from aiogram import Bot, Dispatcher

from core.plugin import BasePlugin


class PluginManager:

    def __init__(
        self,
        bot: Bot,
        dispatcher: Dispatcher,
    ):
        self.bot = bot
        self.dispatcher = dispatcher

        self.plugins: dict[str, BasePlugin] = {}

    def discover(
        self,
        plugins_directory: str = "plugins",
    ) -> None:

        base_path = Path(
            plugins_directory
        )

        for plugin_dir in sorted(
            base_path.iterdir()
        ):

            if not plugin_dir.is_dir():
                continue

            if plugin_dir.name.startswith("_"):
                continue

            plugin_module = (
                plugin_dir / "plugin.py"
            )

            if not plugin_module.exists():
                continue

            self._load_plugin(
                plugin_dir.name
            )

    def _load_plugin(
        self,
        plugin_name: str,
    ) -> None:

        module_path = (
            f"plugins.{plugin_name}.plugin"
        )

        module = importlib.import_module(
            module_path
        )

        plugin_class = None

        for _, obj in inspect.getmembers(
            module,
            inspect.isclass,
        ):

            if (
                issubclass(obj, BasePlugin)
                and obj is not BasePlugin
                and obj.__module__ == module.__name__
            ):
                plugin_class = obj
                break

        if plugin_class is None:
            raise RuntimeError(
                f"No plugin class found in {module_path}"
            )

        plugin = plugin_class(
            bot=self.bot
        )

        plugin.setup()

        self.plugins[plugin.name] = plugin

        print(
            f"Loaded plugin: "
            f"{plugin.name} v{plugin.version}"
        )

    def include_routers(self) -> None:

        for plugin in self.plugins.values():

            self.dispatcher.include_router(
                plugin.router
            )

    async def enable_all(self) -> None:

        for plugin in self.plugins.values():
            await plugin.enable()

    async def disable_all(self) -> None:

        for plugin in self.plugins.values():
            await plugin.disable()