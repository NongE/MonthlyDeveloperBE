from flask import Flask
from flask_restx import Api

from controller import recruit_board, authentication, test


def create_env():
    app = Flask(__name__)

    api = Api(app, version="1.0", title="flask_env", description="flask_env_test")

    # namespace를 추가합니다.
    api.add_namespace(recruit_board.recruit_ns, '/recruit')
    api.add_namespace(authentication.auth_ns, '/login')
    api.add_namespace(test.test_ns, '/test')

    return app
