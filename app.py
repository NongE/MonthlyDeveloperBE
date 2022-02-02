from flask import Flask
from flask_restx import Api

from controller import recruit_controller, login_controller, test_controller


def create_env():
    app = Flask(__name__)

    api = Api(app, version="1.0", title="flask_env", description="flask_env_test")

    # namespace를 추가합니다.
    api.add_namespace(recruit_controller.recruit_ns, '/recruit')
    api.add_namespace(login_controller.login_ns, '/login')
    api.add_namespace(test_controller.test_ns, '/test')

    return app
