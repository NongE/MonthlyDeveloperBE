from datetime import datetime, timedelta
import jwt

from config.env import Env

from model import response_model
response_model = response_model.ResponseModel()

class TokenService:

    def create_token(req_data, user_login, user_email):
        payload = {
                "iss": "MonthlyDeveloper",
                "sub": "UserId",
                "userId": str(user_login) + str(user_email),
                "exp": datetime.utcnow() + timedelta(seconds=Env.ACCESS_TOKEN_EXPIRED_TIME)
        }

        created_token = jwt.encode(payload, Env.SECRET_KEY, Env.ALGORITHM)
        
        return response_model.set_response(req_data.path, 200, "Done", created_token)

    """
        전달받은 토큰이 유효한지 확인하는 함수
        임시로 True 만을 반환하도록 설정
    """
    def validate_token(token):
        try:
            jwt.decode(token, Env.SECRET_KEY, Env.ALGORITHM)
            return True
        except jwt.exceptions.InvalidSignatureError:
            return False

        except jwt.exceptions.ExpiredSignatureError:
            return False
        
        except Exception:
            return False
