import asyncio

from core.bot import create_bot
from core.plugin_manager import PluginManager
from config import config


async def main() -> None:

    token = config.get_required("BOT_TOKEN")
    proxy_url = config.get("PROXY_URL")

    bot, dispatcher = create_bot(
        token=token,
        proxy_url=proxy_url
    )

    plugin_manager = PluginManager(
        bot=bot,
        dispatcher=dispatcher,
    )

    plugin_manager.discover()
    plugin_manager.include_routers()
    await plugin_manager.enable_all()

    print("Bot is running...")

    try:

        await dispatcher.start_polling(bot)

    finally:

        await plugin_manager.disable_all()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())