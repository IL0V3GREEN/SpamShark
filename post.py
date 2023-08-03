from aiohttp import web
from mongo import Database
import requests
from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update


mongo = Database()
crypto = AioCryptoPay("8055:AAXZx66BTYEP7WC2k0Wl9JpR8dmPUF8WOuN", Networks.TEST_NET)


@crypto.pay_handler()
async def hello(update: Update, app):
    text = "Hello!!! 200!!! EVERYTHING OK!!!"
    print(update)
    try:
        return web.Response(text=text)

    except KeyError:
        return web.Response(text="SOME PARAMS MISSING!!!")
