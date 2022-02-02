import bcrypt
import requests

from config.config import Config
from config.connector import Connector

from service.github.github_request import GithubRequest

class LoginService():

    def get_github_user_info(access_code):
        access_token = GithubRequest.request_access_token(access_code)
        user_info = GithubRequest.request_user_info(access_token)
        return user_info

    """
        로그인한 사람이 사용자(서비스 이용자)인지 확인하는 함수
    """
    def is_existing_user(github_user_info):
        db_users = Connector.mongodb_connector().users
        user_info = db_users.find_one({"github_id":str(github_user_info.id)}, {"_id": 0})
        
        if user_info != None:
            if user_info["login"] == str(github_user_info.login) and user_info["email"] == str(github_user_info.email):
                return user_info
        else:
            return False
    
    def save_user(user_info):
        # 서비스에서 고객의 ID는 순차적으로 부여함
        db_user_counter = Connector.mongodb_connector().counter
        user_id = db_user_counter.find_one({"type": "user_counter"}, {"_id": 0})["counter"] + 1

        db_users = Connector.mongodb_connector().users
        try:
            user_info = {   
                "id": user_id,
                "github_id": str(user_info.id),
                "login": str(user_info.login),
                "email": str(user_info.email),
                "approval": True
            }
            db_users.insert_one(user_info)
            db_user_counter.update_one({"type": "user_counter"}, {"$set": {"counter": user_id}})
            return True
        except:
            return False