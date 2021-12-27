from flask_restx import fields, Namespace
from flask_restx import Resource, Namespace

test_ns = Namespace("TEST API", description="동작 테스트를 위한 API")


from service.token_service import TokenService
from datetime import datetime, timedelta
import jwt
from config.env import Env

validate_jwt = test_ns.parser()
validate_jwt.add_argument('header', location='headers')

@test_ns.route('/validate_token', methods=['GET'])
class ValidateToken(Resource):
    @test_ns.expect(validate_jwt)
    def get(self):
        result = TokenService.validate_token(validate_jwt.parse_args()['header'])
        return result

@test_ns.route('/issue_token', methods=['GET'])
class ValidateToken(Resource):
    def get(self):
        payload = {
                "iss": "test_api",
                "sub": "test_id",
                "userId": "test_user_name",
                "exp": datetime.utcnow() + timedelta(seconds=60)
        }

        created_token = jwt.encode(payload, Env.TEST_SECRET_KEY , Env.TEST_ALGORITHM)

        return created_token
    
