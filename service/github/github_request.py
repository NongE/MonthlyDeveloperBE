import requests
from config.config import Config

from model.user_model import UserModel


class GithubRequest():
    """
        Access Code를 활용하여 Access Token을 요청하는 부분
    """
    def request_access_token(access_code):
        
        access_token_param = {
            "client_id": Config.GITHUB_CLIENT_ID,
            "client_secret": Config.GITHUB_CLIENT_SECRET,
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

        user_info = UserModel(info_res.json()['id'], 
                                info_res.json()['login'], 
                                info_res.json()['email'])

        # 응답
        return user_info