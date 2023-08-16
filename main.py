from handlers import start_handler, spamCreate_handlers, parsing_handlers, profile_handlers, info_handlers
import logging
from aiogram import Bot, Dispatcher
from aiohttp import web
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application


BASE_URL = "https://spamshark-production.up.railway.app"
MAIN_BOT_TOKEN = "6249367873:AAFra-Kvtu6i1V9lS8kvx_9J8-XGxDTxCI8"
WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 8532
MAIN_BOT_PATH = "/main.py"


logging.basicConfig(level=logging.INFO)


async def on_startup(bot: Bot):
    await bot.set_webhook(f"{BASE_URL}{MAIN_BOT_PATH}")


def main():
    session = AiohttpSession()
    bot_settings = {"session": session, "parse_mode": "HTML"}
    bot = Bot(token=MAIN_BOT_TOKEN, **bot_settings)
    dp = Dispatcher()
    dp.include_router(start_handler.router)
    dp.include_router(spamCreate_handlers.router)
    dp.include_router(parsing_handlers.router)
    dp.include_router(profile_handlers.router)
    dp.include_router(info_handlers.router)
    dp.startup.register(on_startup)

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=MAIN_BOT_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    main()
