from pymongo import MongoClient
from datetime import datetime


class Database:
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://maximus:08MAXIMUs32@botdata.2yllcxo.mongodb.net/?retryWrites=true&w=majority"
        )
        self.db = self.client.get_database('spamshark')
        self.collection = self.db.get_collection('users')

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
                                'year': datetime.now().strftime("%Y"),
                                'month': datetime.now().strftime("%m"),
                                'day': datetime.now().strftime("%d")
                            },
                            'username': username
                        }
                    }
                }
            }
        )

    def check_parse_available(self, user_id) -> bool:
        orders = self.collection.find_one({'user_id': user_id})['parse_orders']
        count = 0
        for i in orders:
            try:
                order_time = i['date']
                year = order_time['year']
                month = order_time['month']
                day = order_time['day']
                if year == datetime.now().strftime("%Y") \
                        and month == datetime.now().strftime("%m") \
                        and day == datetime.now().strftime("%d"):
                    count += 1
            except KeyError:
                pass

        if count < 3:
            return True
