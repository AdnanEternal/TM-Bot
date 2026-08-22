from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer


def create_bot(
        token: str,
        proxy_url
    ) -> tuple[Bot, Dispatcher]:

    session = None

    if proxy_url:
        session = AiohttpSession(api=TelegramAPIServer.from_base(proxy_url))

    bot = Bot(
        token=token,
        session=session
        )
    dispatcher = Dispatcher()

    return bot, dispatcher