import os
import pathlib
from pyrogram import Client
from mongo import Database


db = Database()
proxy = {
    'scheme': 'socks5',
    'hostname': '5.252.30.204',
    'port': 3001,
    'username': '6pZ0th',
    'password': 'wI49jMp6ne'
}


class Sessions:
    @staticmethod
    async def valid_sessions():
        current_dir = pathlib.Path('.')
        current_pattern = "*.session"
        sessions = list(current_dir.glob(current_pattern))
        available = 0
        files = []
        for session in sessions:
            app = Client(
                session.name.split(".")[0],
                db.find_session(session.name, 'api_id'),
                db.find_session(session.name, 'api_hash'),
                proxy=db.current_proxy()
            )
            try:
                try:
                    if await app.connect():
                        profile = await app.get_me()
                        if not profile.is_restricted and not profile.is_deleted:
                            available += 1
                        else:
                            files.append(session.name)
                    else:
                        files.append(session.name)
                except ConnectionError:
                    available += 1
            except AttributeError:
                files.append(session.name)
        for file in files:
            os.remove(file)
            db.delete_session(file)

        return available

    @staticmethod
    async def spammers_sessions():
        current_dir = pathlib.Path('.')
        current_pattern = "*.session"
        sessions = list(current_dir.glob(current_pattern))
        available = 0
        files = []
        for session in sessions:
            app = Client(
                session.name.split(".")[0],
                db.find_session(session.name, 'api_id'),
                db.find_session(session.name, 'api_hash'),
                proxy=db.current_proxy()
            )
            try:
                try:
                    if await app.connect():
                        profile = await app.get_me()
                        if profile.is_restricted and not profile.is_deleted:
                            available += 1
                        else:
                            pass
                    else:
                        files.append(session.name)
                except ConnectionError:
                    available += 1
            except AttributeError:
                files.append(session.name)
        for file in files:
            os.remove(file)
            db.delete_session(file)

        return available

