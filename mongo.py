from pymongo import MongoClient
from datetime import datetime
import pytz


class Database:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://maximus:08MAXIMUs32@botdata.2yllcxo.mongodb.net/?retryWrites=true&w=majority"
        )
        self.db = self.client.get_database('spamshark')
        self.collection = self.db.get_collection('users')
        self.db2 = self.client.get_database('spamshark')
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

    def create_spam_order(self, order_uid, user_id, value, theme):
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

    def get_order_info(self, order_uid):
        return self.orders.find_one({'order_uid': order_uid})

    def get_current_price(self) -> float:
        return self.collection.find_one({'message_price': 'message_price'})['price']
