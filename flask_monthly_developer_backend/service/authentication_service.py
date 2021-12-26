import requests

from config.env import Env


class AuthenticationService():

    """
        Access Code를 활용하여 Access Token을 요청하는 부분
    """
    def request_access_token(access_code):
        
        access_token_param = {
            "client_id": Env.GITHUB_CLIENT_ID,
            "client_secret": Env.GITHUB_CLIENT_SECRET,
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
        return True