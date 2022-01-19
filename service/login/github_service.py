import os
import bcrypt
from dotenv import load_dotenv

from config.db_config import DBConfig

import requests

load_dotenv()

class GithubService():

    """
        Access Code를 활용하여 Access Token을 요청하는 부분
    """
    def request_access_token(access_code):
        
        access_token_param = {
            "client_id": os.environ.get("GITHUB_CLIENT_ID"),
            "client_secret": os.environ.get("GITHUB_CLIENT_SECRET"),
            "code": access_code
        }

        # 요청에 대한 응답을 json으로 받기 위해 header 설정
        access_token_req_header = {"Accept": "application/json"}

        # Access Token request
        access_token_req_url = f"https://github.com/login/oauth/access_token"
        access_token_res = requests.post(access_token_req_url, headers=access_token_req_header, data=access_token_param)

        # Access Token 확인
        access_token = access_token_res.json()['access_token']

        return access_token

    """
        Access Token을 활용하여 사용자 정보를 요청하는 부분
    """
    def request_user_info(access_token):

        # Header 에 Token을 설정
        info_header = {
            "Authorization": f"token {access_token}"
        }

        # User Info request
        info_req_url = f"https://api.github.com/user"
        info_res = requests.get(info_req_url, headers=info_header)

        user_login = info_res.json()['login']
        user_email = info_res.json()['email']

        # 응답
        return user_login, user_email

    """
        로그인한 사람이 사용자(서비스 이용자)인지 확인하는 함수
        임시로 True 만을 반환하도록 설정
    """
    def vaildate_user(user_login, user_email):
        
        wmd_users = DBConfig.mongo_config().wmd_users
        
        users_data = wmd_users.find({"email":user_email}, {"_id": 0})

        data = [doc for doc in users_data]
        
        if len(data) == 1:
            if bcrypt.checkpw(str(user_login).encode("utf-8"), data[0]['login']):
                print("is already!")
                return True
            else:
                return False
        elif len(data) == 0:
            
            hash_user_login = bcrypt.hashpw(str(user_login).encode("utf-8"), bcrypt.gensalt())

            user_info = {
                "login": hash_user_login,
                "email": user_email
            }

            wmd_users.insert_one(user_info)

            return True
        else:
            return False
    