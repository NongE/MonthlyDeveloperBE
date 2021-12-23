import requests

from flask import url_for, redirect, request
from flask_restx import Resource, Namespace

from config.env import Env
from model import authentication_model

"""
Authlib을 사용하지 않고 구현
로그인 URL: ~/login/test
"""
Auth = authentication_model.AuthenticationModel()
auth_ns = Auth.auth_ns
github_access_code_parser = Auth.github_access_code_parser
create_jwt_model = Auth.create_jwt_model
validate_jwt = Auth.validate_jwt

# 사용자가 로그인 할 때 접속하는 URL (http://localhost:5000/login/test)
@auth_ns.route('/github', methods=['GET'], doc=False)
class Github(Resource):
    def get(self):
        # Github 측으로 로그인하고 Access Code를 받기 위해 redirect 설정
        redirect_uri = f"http://github.com/login/oauth/authorize?client_id={Env.GITHUB_CLIENT_ID}&redirect_uri={Env.REDIRECT_URL}"
        # 로그인을 위한 redirect
        return redirect(redirect_uri)

# Access Code를 전달받기 위한 URL (http://localhost:5000/login/callback)
@auth_ns.route('/callback', methods=['GET'])
class RedirectTest(Resource):
    @auth_ns.expect(github_access_code_parser)
    def get(self):
        # Access Code는 Query param 의 형태로 떨어짐
        # request.args.get('code') 부분
        access_token_param = {
            "client_id": Env.GITHUB_CLIENT_ID,
            "client_secret": Env.GITHUB_CLIENT_SECRET,
            "code": github_access_code_parser.parse_args()["code"]
        }

        """
        이하 Access Code를 활용하여 Access Token을 요청하는 부분
        """
        # 요청에 대한 응답을 json으로 받기 위해 header 설정
        access_token_req_header = {"Accept": "application/json"}

        # Access Token request
        access_token_req_url = f"https://github.com/login/oauth/access_token"
        access_token_res = requests.post(access_token_req_url, headers=access_token_req_header, data=access_token_param)

        # Access Token 확인
        print(access_token_res.json())
        print(access_token_res.json()['access_token'])

        """
        이하 Access Token을 활용하여 사용자 정보를 요청하는 부분
        """

        # Header 에 Token을 설정
        info_header = {
            "Authorization": f"token {access_token_res.json()['access_token']}"
        }

        # User Info request
        info_req_url = f"https://api.github.com/user"
        info_res = requests.get(info_req_url, headers=info_header)

        # 결과 확인
        print(info_res.json())

        # 응답
        return f"User name: {info_res.json()['login']} User E-main: {info_res.json()['email']}"


"""
JWT TEST
"""
import jwt
from datetime import datetime, timedelta


@auth_ns.route('/create_token', methods=['POST'])
class CreateToken(Resource):
    @auth_ns.expect(create_jwt_model, validate=True)
    def post(self):

        payload = {
            "iss": "MonthlyDeveloper",
            "sub": "UserId",
            "userId": request.json["login"] + request.json["email"],
            "exp": datetime.utcnow() + timedelta(seconds=60)
        }

        token = jwt.encode(payload, Env.SECRET_KEY, Env.ALGORITHM)

        result = {
            "token": token
        }

        return result


@auth_ns.route('/validate_token')
class ValidateToken(Resource):
    @auth_ns.expect(validate_jwt)
    def get(self):
        result = {
            "decode_token": jwt.decode(validate_jwt.parse_args()['header'], Env.SECRET_KEY, Env.ALGORITHM)
        }

        return result
