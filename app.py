from flask import Flask
from flask_restx import Api

from controller import test_controller
from controller.board import recruit_controller
from controller.login import github_controller


def create_env():
    app = Flask(__name__)

    api = Api(app, version="1.0", title="flask_env", description="flask_env_test")

    # namespace를 추가합니다.
    api.add_namespace(recruit_controller.recruit_ns, '/recruit')
    api.add_namespace(github_controller.auth_ns, '/login')
    api.add_namespace(test_controller.test_ns, '/test')

    return app
