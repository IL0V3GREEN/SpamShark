from pymongo import MongoClient
from datetime import datetime, timedelta
from operator import itemgetter
import pytz


class Database:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://maximus:08MAXIMUs32@botdata.2yllcxo.mongodb.net/?retryWrites=true&w=majority"
        )
        self.db = self.client.get_database('spamshark')
        self.collection = self.db.get_collection('users')
        self.orders = self.db.get_collection('orders')
        self.functions = self.db.get_collection('functions')
        self.session = self.db.get_collection('sessions')
        self.tz = pytz.timezone("Europe/Moscow")

    def user_exists(self, user_id):
        result = self.collection.find_one({'user_id': user_id})
        try:
            return bool(len(result))
        except TypeError:
            return False

    def add_user(self, user_id, username):
        self.collection.insert_one(
            {
                'user_id': user_id,
                'username': username,
                'balance': 0,
                'rating': Database().count_rating(user_id),
                'date': {
                    'year': datetime.now(self.tz).strftime("%Y"),
                    'month': datetime.now(self.tz).strftime("%m"),
                    'day': datetime.now(self.tz).strftime("%d")
                }
            }
        )

    def user_info(self, user_id):
        return self.collection.find_one({'user_id': user_id})

    def update_string(self, user_id, string):
        self.collection.update_one(
            {'user_id': user_id},
            {"$set": string}
        )

    def create_spam_order(self, order_uid, user_id, value: int, theme, price):
        self.orders.insert_one(
            {
                'order_uid': order_uid,
                'user_id': user_id,
                'messages': value,
                'theme': theme,
                'price': price,
                'date': {
                    'year': datetime.now(self.tz).strftime("%Y"),
                    'month': datetime.now(self.tz).strftime("%m"),
                    'day': datetime.now(self.tz).strftime("%d")
                }
            }
        )

    def count_today(self, user_id) -> len:
        today_orders = []
        for order in list(self.orders.find({'user_id': user_id})):
            if order['date']['year'] == datetime.now(self.tz).strftime("%Y") and \
                    order['date']['month'] == datetime.now(self.tz).strftime("%m") and \
                    order['date']['day'] == datetime.now(self.tz).strftime("%d"):
                today_orders.append(order)
        return len(today_orders)

    def earned_today(self) -> float:
        earned = 0
        for order in list(self.orders.find()):
            if order['date']['year'] == datetime.now(self.tz).strftime("%Y") and \
                    order['date']['month'] == datetime.now(self.tz).strftime("%m") and \
                    order['date']['day'] == datetime.now(self.tz).strftime("%d"):
                earned += order['price']
        return earned

    def users_joined_today(self) -> len:
        users = []
        for user in list(self.collection.find()):
            if user['date']['year'] == datetime.now(self.tz).strftime("%Y") and \
                    user['date']['month'] == datetime.now(self.tz).strftime("%m") and \
                    user['date']['day'] == datetime.now(self.tz).strftime("%d"):
                users.append(user)
        return len(users)

    def count_week(self, user_id) -> len:
        week_orders = []
        for order in list(self.orders.find({'user_id': user_id})):
            order_time = datetime(
                int(order['date']['year']),
                int(order['date']['month']),
                int(order['date']['day'])
            ).timestamp()

            if order_time in range(
                    int((datetime.now(self.tz) - timedelta(days=7)).timestamp()),
                    int(datetime.now(self.tz).timestamp())
            ):
                week_orders.append(order)

        return len(week_orders)

    def earned_week(self) -> float:
        earned = 0
        for order in list(self.orders.find()):
            order_time = datetime(
                int(order['date']['year']),
                int(order['date']['month']),
                int(order['date']['day'])
            ).timestamp()
            if order_time in range(
                    int((datetime.now(self.tz) - timedelta(days=7)).timestamp()),
                    int(datetime.now(self.tz).timestamp())
            ):
                earned += order['price']
        return earned

    def users_joined_week(self) -> len:
        users = []
        for user in list(self.collection.find()):
            joined_time = datetime(
                int(user['date']['year']),
                int(user['date']['month']),
                int(user['date']['day'])
            ).timestamp()
            if joined_time in range(
                    int((datetime.now(self.tz) - timedelta(days=7)).timestamp()),
                    int(datetime.now(self.tz).timestamp())
            ):
                users.append(user)
        return len(users)

    def count_month(self, user_id) -> len:
        month_orders = []
        for order in list(self.orders.find({'user_id': user_id})):
            order_time = datetime(
                int(order['date']['year']),
                int(order['date']['month']),
                int(order['date']['day'])
            ).timestamp()

            if order_time in range(
                    int((datetime.now(self.tz) - timedelta(days=30)).timestamp()),
                    int(datetime.now(self.tz).timestamp())
            ):
                month_orders.append(order)

        return len(month_orders)

    def earned_month(self) -> float:
        earned = 0
        for order in list(self.orders.find()):
            order_time = datetime(
                int(order['date']['year']),
                int(order['date']['month']),
                int(order['date']['day'])
            ).timestamp()

            if order_time in range(
                    int((datetime.now(self.tz) - timedelta(days=30)).timestamp()),
                    int(datetime.now(self.tz).timestamp())
            ):
                earned += order['price']
        return earned

    def users_joined_month(self) -> len:
        users = []
        for user in list(self.collection.find()):
            joined_time = datetime(
                int(user['date']['year']),
                int(user['date']['month']),
                int(user['date']['day'])
            ).timestamp()
            if joined_time in range(
                    int((datetime.now(self.tz) - timedelta(days=30)).timestamp()),
                    int(datetime.now(self.tz).timestamp())
            ):
                users.append(user)
        return len(users)

    def earned_alltime(self) -> float:
        earned = 0
        for order in list(self.orders.find()):
            earned += order['price']
        return earned

    def count_all_messages(self, user_id) -> int:
        orders = list(self.orders.find({'user_id': user_id}))
        messages = 0
        for order in orders:
            messages += order['messages']
        return messages

    def count_rating(self, user_id) -> int:
        return len(list(self.orders.find({'user_id': user_id}))) + Database().count_referrals(user_id) * 10

    def top_rating_list(self):
        all_users = list(self.collection.find())
        top_users = []
        string = ""
        for user in all_users:
            if user['rating'] > 0:
                top_users.append(user)
        result = sorted(top_users, key=itemgetter('rating'), reverse=True)
        if len(result) >= 10:
            for count in range(0, 10):
                if count == 0:
                    place = "🥇"
                elif count == 1:
                    place = "🥈"
                elif count == 2:
                    place = "🥉"
                else:
                    place = f"{count + 1}."
                string += f"{place} <b>{result[count]['username']}</b> - <code>{result[count]['rating']}</code>\n"
        else:
            for count in range(len(result)):
                if count == 0:
                    place = "🥇"
                elif count == 1:
                    place = "🥈"
                elif count == 2:
                    place = "🥉"
                else:
                    place = f"{count + 1}."
                string += f"{place} <b>{result[count]['username']}</b> - <code>{result[count]['rating']}</code>\n"

        return string

    def count_referrals(self, user_id) -> int:
        return len(list(self.collection.find({'ref_id': user_id})))

    def get_order_info(self, order_uid):
        return self.orders.find_one({'order_uid': order_uid})

    def get_current_price(self) -> float:
        return self.collection.find_one({'message_price': 'message_price'})['price']

    def get_shop_status(self):
        return self.functions.find_one({"shop_status": "shop_status"})['status']

    def change_shop_status(self):
        if Database().get_shop_status() == "enabled":
            self.functions.update_one({"shop_status": "shop_status"}, {"$set": {'status': 'disabled'}})
        elif Database().get_shop_status() == "disabled":
            self.functions.update_one({"shop_status": "shop_status"}, {"$set": {'status': 'enabled'}})

    def add_session(self, name: str, api_id: int, api_hash: str):
        self.session.insert_one(
            {
                'session_name': name,
                'api_id': api_id,
                'api_hash': api_hash
            }
        )

    def find_session(self, name: str):
        return self.session.find_one({'session_name': name})

    def delete_session(self, name: str):
        self.session.delete_one({'session_name': name})

    def current_proxy(self) -> dict:
        return self.functions.find_one({'proxy': 'proxy'})['current']

    def update_proxy(self, scheme: str, hostname: str, port: int, username: str, password: str):
        self.functions.update_one(
            {'proxy': 'proxy'},
            {
                "$set": {
                    'current': {
                        'scheme': scheme,
                        'hostname': hostname,
                        'port': port,
                        'username': username,
                        'password': password
                    }
                }
            }
        )
