from flask_restx import Namespace


class LoginModel:
    login_ns = Namespace("Github Login", description="Github Oauth를 활용한 로그인")

    github_callback_parser = login_ns.parser()
    github_callback_parser.add_argument('code')