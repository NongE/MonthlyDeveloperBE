from pymongo import MongoClient

from config.config import Config


class Connector:
    @staticmethod
    def mongodb_connector():
        return MongoClient(Config.MONGO_URI)[Config.DB_NAME]
