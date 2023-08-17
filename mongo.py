from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz


class Database:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://maximus:08MAXIMUs32@botdata.2yllcxo.mongodb.net/?retryWrites=true&w=majority"
        )
        self.db = self.client.get_database('spamshark')
        self.collection = self.db.get_collection('users')
        self.orders = self.db.get_collection('orders')
        self.tz = pytz.timezone("Europe/Moscow")

    def user_exists(self, user_id):
        result = self.collection.find_one({'user_id': user_id})
        try:
            return bool(len(result))
        except TypeError:
            return False

    def add_user(self, user_id):
        self.collection.insert_one(
            {
                'user_id': user_id,
                'balance': 0
            }
        )

    def user_info(self, user_id):
        return self.collection.find_one({'user_id': user_id})

    def update_string(self, user_id, string):
        self.collection.update_one(
            {'user_id': user_id},
            {"$set": string}
        )

    def create_spam_order(self, order_uid, user_id, value: int, theme):
        self.orders.insert_one(
            {
                'order_uid': order_uid,
                'user_id': user_id,
                'messages': value,
                'theme': theme,
                'date': {
                    'year': datetime.now(self.tz).strftime("%Y"),
                    'month': datetime.now(self.tz).strftime("%m"),
                    'day': datetime.now(self.tz).strftime("%d")
                }
            }
        )

    def count_today(self, user_id) -> len:
        orders = list(self.orders.find({'user_id': user_id}))
        today_orders = []
        for order in orders:
            if order['date']['year'] == datetime.now(self.tz).strftime("%Y") and \
                    order['date']['month'] == datetime.now(self.tz).strftime("%m") and \
                    order['date']['day'] == datetime.now(self.tz).strftime("%d"):
                today_orders.append(order)

        return len(today_orders)

    def count_week(self, user_id) -> len:
        today = int(datetime.now(self.tz).timestamp())
        time_7_day_before = int((datetime.now(self.tz) - timedelta(days=7)).timestamp())
        orders = list(self.orders.find({'user_id': user_id}))
        week_orders = []
        for order in orders:
            order_time = datetime(
                int(order['date']['year']),
                int(order['date']['month']),
                int(order['date']['day'])
            ).timestamp()

            if order_time in range(time_7_day_before, today):
                week_orders.append(order)

        return len(week_orders)

    def count_month(self, user_id) -> len:
        today = int(datetime.now(self.tz).timestamp())
        time_30_day_before = int((datetime.now(self.tz) - timedelta(days=30)).timestamp())
        orders = list(self.orders.find({'user_id': user_id}))
        month_orders = []
        for order in orders:
            order_time = datetime(
                int(order['date']['year']),
                int(order['date']['month']),
                int(order['date']['day'])
            ).timestamp()

            if order_time in range(time_30_day_before, today):
                month_orders.append(order)

        return len(month_orders)

    def count_all_messages(self, user_id) -> int:
        orders = list(self.orders.find({'user_id': user_id}))
        messages = 0
        for order in orders:
            messages += order['messages']
        return messages

    def count_rating(self, user_id) -> int:
        result = len(list(self.orders.find({'user_id': user_id}))) + (Database().count_referrals(user_id) * 10)
        return result

    def count_referrals(self, user_id) -> int:
        return len(list(self.collection.find({'ref_id': user_id})))

    def get_order_info(self, order_uid):
        return self.orders.find_one({'order_uid': order_uid})

    def get_current_price(self) -> float:
        return self.collection.find_one({'message_price': 'message_price'})['price']
