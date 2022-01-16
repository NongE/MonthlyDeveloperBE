import os
from dotenv import load_dotenv

from pymongo import MongoClient

load_dotenv()


class DBConfig:

    @staticmethod
    def mongo_config():
        return MongoClient(os.environ.get("MONGO_URI"))[os.environ.get("DB_NAME")]
