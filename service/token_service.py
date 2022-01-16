import os
from dotenv import load_dotenv

from datetime import datetime, timedelta
import jwt


from model import response_model
response_model = response_model.ResponseModel()

load_dotenv()


class TokenService:

    def create_token(req_data, user_login, user_email):
        payload = {
                "iss": "MonthlyDeveloper",
                "sub": "UserId",
                "userId": str(user_login) + str(user_email),
                "exp": datetime.utcnow() + timedelta(seconds=int(os.environ.get("ACCESS_TOKEN_EXPIRED_TIME")))
        }

        created_token = jwt.encode(payload, os.environ.get("SECRET_KEY"), os.environ.get("ALGORITHM"))
        
        return response_model.set_response(req_data.path, 200, "Done", created_token)

    """
        전달받은 토큰이 유효한지 확인하는 함수
        임시로 True 만을 반환하도록 설정
    """
    def validate_token(token):
        try:
            jwt.decode(token, os.environ.get("SECRET_KEY"), os.environ.get("ALGORITHM"))
            return True
        except jwt.exceptions.InvalidSignatureError:
            return False

        except jwt.exceptions.ExpiredSignatureError:
            return False
        
        except Exception:
            return False