from flask import Flask
from flask_restx import Api

import os

from controller import recruit_board, authentication

def create_env():
    app = Flask(__name__)

    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = os.urandom(24)

    api = Api(app, version=1.0, title="flask_env", description="flask_env_test")

    # namespace를 추가합니다.
    api.add_namespace(recruit_board.recruit_ns, '/recruit')
    api.add_namespace(authentication.auth_ns, '/login')

    return app
