import asyncio

from aiogram import Router

from core.bot import create_bot
from core.plugin_manager import PluginManager
from core.event_manager import EventManager
from core.database_manager import DatabaseManager

from config import config

async def main() -> None:

    token = config.get_required("BOT_TOKEN")
    proxy_url = config.get("PROXY_URL",default='')

    bot, dispatcher = create_bot(
        token=token,
        proxy_url=proxy_url,
    )
    db = DatabaseManager()
    await db.connect()

    plugin_manager = PluginManager(
        bot=bot,
        dispatcher=dispatcher,
        db=db,
    )

    await plugin_manager.initialize()
    plugin_manager.discover()

    await plugin_manager.enable_all()
    await plugin_manager.command_manager.sync_commands(bot)
    plugin_manager.include_command_router()

    event_manager = EventManager(
        plugin_manager.plugins.values()
    )

    fallback_router = Router(name="fallback")
    fallback_router.message.register(event_manager.handle_message)
    dispatcher.include_router(fallback_router)

    print("Bot is running...")
    

    try:
        await dispatcher.start_polling(bot)


    finally:
        await plugin_manager.disable_all()
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())