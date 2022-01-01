import jwt
from datetime import datetime, timedelta

from flask_restx import fields, Namespace, Resource



from config.env import Env

from .controller_decorator import validate_token_decorator

test_ns = Namespace("TEST API", description="동작 테스트를 위한 API")

validate_jwt = test_ns.parser()
validate_jwt.add_argument('header', location='headers')


@test_ns.route('/get_validate_token', methods=['GET'])
class GetValidateToken(Resource):
    @test_ns.expect(validate_jwt)
    @validate_token_decorator
    def get(self):
        return {"result": "validate Header/Token"}

@test_ns.route('/post_validate_token', methods=['POST'])
class PostValidateToken(Resource):
    @test_ns.expect(validate_jwt)
    @validate_token_decorator
    def post(self):
        return {"result": "post method validate Header/Token"}

@test_ns.route('/issue_token', methods=['GET'])
class IssueToken(Resource):
    def get(self):
        payload = {
                "iss": "test_api",
                "sub": "test_id",
                "userId": "test_user_name",
                "exp": datetime.utcnow() + timedelta(seconds=Env.ACCESS_TOKEN_EXPIRED_TIME)
        }

        created_token = jwt.encode(payload, Env.TEST_SECRET_KEY , Env.TEST_ALGORITHM)

        return created_token
    
