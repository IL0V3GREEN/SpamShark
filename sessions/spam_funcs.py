from pyrogram import Client
from mongo import Database


db = Database()


class Sessions:
    @staticmethod
    async def valid_sessions():
        sessions = list(db.session.find())
        available = 0
        files = []
        if len(sessions) != 0:
            for session in sessions:
                app = Client(
                    session['session_name'].split(".")[0],
                    session['api_id'],
                    session['api_hash'],
                    proxy=db.current_proxy()
                )
                try:
                    try:
                        if await app.connect():
                            profile = await app.get_me()
                            if not profile.is_restricted and not profile.is_deleted:
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
                db.delete_session(file)

        return available

    @staticmethod
    async def spammers_sessions():
        sessions = list(db.session.find())
        available = 0
        files = []
        if len(sessions) != 0:
            for session in sessions:
                app = Client(
                    session['session_name'].split(".")[0],
                    session['api_id'],
                    session['api_hash'],
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
                db.delete_session(file)

        return available
