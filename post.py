from aiohttp import web
from mongo import Database
import requests

mongo = Database()


async def hello(request):
    print(request)
    try:
        return web.Response(text="Hello!!! 200!!! EVERYTHING OK!!!")

    except KeyError:
        return web.Response(text="SOME PARAMS MISSING!!!")
