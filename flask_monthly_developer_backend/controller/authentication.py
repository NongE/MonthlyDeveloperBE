import requests

from flask import url_for, redirect, request
from flask_restx import Resource, Namespace
from authlib.integrations.flask_client import OAuth
from config.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

oauth = OAuth()

auth_ns = Namespace("Github Oauth", description="Github Oauth 로그인")

github = oauth.register(
    name='github',
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# Github login route
@auth_ns.route('/github', methods=['GET'])
class GithubLogin(Resource):
    def get(self):
        github_ = oauth.create_client('github')
        redirect_uri = url_for('Github Oauth_github_authorize', _external=True)
        return github_.authorize_redirect(redirect_uri)


# Github authorize route
@auth_ns.route('/github/authorize', methods=['GET'])
class GithubAuthorize(Resource):
    def get(self):

        # github_ = oauth.create_client('github')
        # access_token = github_.authorize_access_token()['access_token']
        # 위와 같은 식으로도 사용 가능

        access_token = oauth.github.authorize_access_token()['access_token']
        resp = oauth.github.get('user').json()

        user_ID, email = resp['login'], resp['email']

        return f"You are successfully signed in using github, user_ID : {user_ID} / E-mail : {email}"


"""

Authlib을 사용하지 않고 구현한 부분

로그인 URL: http://localhost:8000/login/test

"""


# 사용자가 로그인 할 때 접속하는 URL (http://localhost:8000/login/test)
@auth_ns.route('/test', methods=['GET'])
class test(Resource):
    def get(self):

        # Github 측으로 로그인하고 Access Code를 받기 위해 redirect 설정
        redirect_uri = f"http://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri=http://localhost:8000/login/callback"

        # 로그인을 위한 redirect
        return redirect(redirect_uri)

# Access Code를 전달받기 위한 URL (http://localhost:8000/login/callback)
@auth_ns.route('/callback', methods=['GET'])
class RedirectTest(Resource):
    def get(self):
        
        # Access Code는 Query param 의 형태로 떨어짐
        # request.args.get('code') 부분
        access_token_param = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": request.args.get('code')
        }

        """
        이하 Access Code를 활용하여 Access Token을 요청하는 부분
        """
        # 요청에 대한 응답을 json으로 받기 위해 header 설정
        access_token_req_header = {"Accept": "application/json"}

        # Access Token request
        access_token_req_url = f"https://github.com/login/oauth/access_token"
        access_token_res = requests.post(access_token_req_url, headers = access_token_req_header, data = access_token_param)
        
        # Access Token 확인
        print(access_token_res.json())
        print(access_token_res.json()['access_token'])

        """
        이하 Access Token을 활용하여 사용자 정보를 요청하는 부분
        """

        # Header 에 Token을 설정
        info_header = {
            "Authorization": f"token {access_code_res.json()['access_token']}"
        }

        # User Info request
        info_req_url = f"https://api.github.com/user"
        info_res = requests.get(info_req_url, headers = info_header)
        
        # 결과 확인
        print(info_res.json())

        # 응답
        return f"User name: {info_res.json()['login']} User E-main: {info_res.json()['email']}"