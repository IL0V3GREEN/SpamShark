import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import start_handler, spamCreate_handlers, parsing_handlers, balance_handlers


TOKEN = "6249367873:AAFra-Kvtu6i1V9lS8kvx_9J8-XGxDTxCI8"


dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode="HTML")
    dp.include_router(start_handler.router)
    dp.include_router(spamCreate_handlers.router)
    dp.include_router(parsing_handlers.router)
    dp.include_router(balance_handlers.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
