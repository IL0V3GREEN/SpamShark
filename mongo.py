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
                'balance': 0,
                'parse_orders': [],
                'spam_orders': []
            }
        )

    def user_info(self, user_id):
        return self.collection.find_one({'user_id': user_id})

    def update_string(self, user_id, string):
        self.collection.update_one(
            {'user_id': user_id},
            {"$set": string}
        )

    def create_parse_order(self, user_id, username):
        count = len(self.collection.find_one({'user_id': user_id})['parse_orders'])
        self.collection.update_one(
            {'user_id': user_id},
            {
                '$addToSet': {
                    'parse_orders': {
                        f'order_{count}': {
                            'date': {
                                'year': datetime.now(self.tz).strftime("%Y"),
                                'month': datetime.now(self.tz).strftime("%m"),
                                'day': datetime.now(self.tz).strftime("%d")
                            },
                            'username': username
                        }
                    }
                }
            }
        )

    def create_spam_order(self, user_id):
        count = len(self.collection.find_one({'user_id': user_id})['parse_orders'])
        self.collection.update_one(
            {'user_id': user_id},
            {
                '$addToSet': {
                    'spam_orders': {
                        f'order_{count}': {
                            'date': {
                                'year': datetime.now(self.tz).strftime("%Y"),
                                'month': datetime.now(self.tz).strftime("%m"),
                                'day': datetime.now(self.tz).strftime("%d")
                            }
                        }
                    }
                }
            }
        )

    def check_parse_available(self, user_id):
        orders = self.collection.find_one({'user_id': user_id})['parse_orders']
        ord_count = 0
        count = 0
        for i in orders:
            if i[f'order_{ord_count}']['date']['year'] == datetime.now(self.tz).strftime("%Y") and \
                    i[f'order_{ord_count}']['date']['month'] == datetime.now(self.tz).strftime("%m") and \
                    i[f'order_{ord_count}']['date']['day'] == datetime.now(self.tz).strftime("%d"):
                count += 1
            ord_count += 1

        if count < 3:
            return True

        return False

    def get_current_price(self):
        return self.collection.find_one({'message_price': 'message_price'})['price']
