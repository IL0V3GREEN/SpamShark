from pymongo import MongoClient


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
