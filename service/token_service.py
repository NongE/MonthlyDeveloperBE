import jwt
from datetime import datetime, timedelta

from config.config import Config
from model.response_model import ResponseModel

class TokenService:

    def create_token(req_data, user_info):
        created_token = jwt.encode(user_info, Config.SECRET_KEY, Config.ALGORITHM)
        return ResponseModel.set_response(req_data.path, 200, "Done", created_token)

    """
        전달받은 토큰이 유효한지 확인하는 함수
        임시로 True 만을 반환하도록 설정
    """
    def validate_token(token):
        try:
            jwt.decode(token, Config.SECRET_KEY, Config.ALGORITHM)
            return True
        except jwt.exceptions.InvalidSignatureError:
            return False

        except jwt.exceptions.ExpiredSignatureError:
            return False
        
        except Exception:
            return False