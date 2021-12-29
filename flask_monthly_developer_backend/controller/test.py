import jwt
from datetime import datetime, timedelta

from flask_restx import fields, Namespace, Resource

from service.token_service import TokenService

from config.env import Env


test_ns = Namespace("TEST API", description="동작 테스트를 위한 API")

validate_jwt = test_ns.parser()
validate_jwt.add_argument('header', location='headers')

from functools import wraps
from flask import request

def validate_token_decorator(func):
    @wraps(func)
    def validste(*args, **kwargs):
        try:
            print(request.headers["Header"])
            return func(*args, **kwargs)
        except:
            return {"result": "Not Found Header/Token"}
    return validste


@test_ns.route('/validate_token', methods=['GET'])
class ValidateToken(Resource):
    @test_ns.expect(validate_jwt)
    @validate_token_decorator
    def get(self):
        result = TokenService.validate_token(validate_jwt.parse_args()['header'])
        return result

@test_ns.route('/issue_token', methods=['GET'])
class IssueToken(Resource):
    def get(self):
        payload = {
                "iss": "test_api",
                "sub": "test_id",
                "userId": "test_user_name",
                "exp": datetime.utcnow() + timedelta(seconds=60)
        }

        created_token = jwt.encode(payload, Env.TEST_SECRET_KEY , Env.TEST_ALGORITHM)

        return created_token
    
