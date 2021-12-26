import requests

from flask import url_for, redirect, request
from flask_restx import Resource, Namespace

from config.env import Env
from model import authentication_model

from service.authentication_service import AuthenticationService
from service.token_service import TokenService

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

        # callback으로 내려온 access code를 저장
        access_code = github_access_code_parser.parse_args()["code"]

        # 전달받은 access code를 활용하여 access token 요청
        access_token = AuthenticationService.request_access_token(access_code)

        # 발급받은 access token을 활용하여 사용자 정보 요청
        user_login, user_email = AuthenticationService.request_user_info(access_token)

        # 로그인한 사용자가 서비스 이용자인지 확인
        if AuthenticationService.vaildate_user(user_login, user_email):
            # 신규회원, 기존회원일 시 토큰 생성
            access_token = TokenService.create_token(user_login, user_email)
        
        # 응답
        return {
            "User Login": user_login,
            "User E-mail": user_email,
            "Access Token": access_token
        }


"""
JWT TEST
"""

import jwt

@auth_ns.route('/validate_token')
class ValidateToken(Resource):
    @auth_ns.expect(validate_jwt)
    def get(self):
        result = {
            "decode_token": jwt.decode(validate_jwt.parse_args()['header'], Env.SECRET_KEY, Env.ALGORITHM)
        }

        return result
