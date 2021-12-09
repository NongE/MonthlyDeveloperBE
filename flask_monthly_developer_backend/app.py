from flask import Flask
from flask_restx import Api

import os

from controller import recruit_board, authentication
from controller.authentication import oauth
from config import config
from config import db_connector

def create_env():
    app = Flask(__name__)

    # MongoDB 연결을 설정합니다.
    app.config['MONGO_URI'] = config.MONGO_URI
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    db_connector.mongo.init_app(app)

    oauth.init_app(app)

    api = Api(app, version=1.0, title="flask_env", description="flask_env_test")
    # app.register_blueprint(auth, url_prefix='/')

    # namespace를 추가합니다.
    api.add_namespace(recruit_board.recruit_ns, '/recruit')
    api.add_namespace(authentication.auth_ns, '/login')

    return app
