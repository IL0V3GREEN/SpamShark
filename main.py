from aiocryptopay import AioCryptoPay, Networks
from handlers import start_handler, spamCreate_handlers, parsing_handlers, balance_handlers
from middlewares.add_user_middleware import CounterMiddleware
import logging
from post import hello
from aiogram import Bot, Dispatcher
from aiohttp import web
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application


crypto = AioCryptoPay("8055:AAXZx66BTYEP7WC2k0Wl9JpR8dmPUF8WOuN", Networks.TEST_NET)

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
    dp.message.outer_middleware.register(CounterMiddleware())
    dp.include_router(start_handler.router)
    dp.include_router(spamCreate_handlers.router)
    dp.include_router(parsing_handlers.router)
    dp.include_router(balance_handlers.router)
    dp.startup.register(on_startup)

    app = web.Application()
    app.add_routes([web.post("/8055:AAXZx66BTYEP7WC2k0Wl9JpR8dmPUF8WOuN", crypto.get_updates)])
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=MAIN_BOT_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    main()
