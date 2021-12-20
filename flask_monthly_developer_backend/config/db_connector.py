from pymongo import MongoClient

from config.env import Env

mongo = MongoClient(Env.MONGO_URI)[Env.DB_NAME]