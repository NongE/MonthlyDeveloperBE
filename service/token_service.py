import jwt
from datetime import datetime, timedelta

from config.config import Config
from model.response_model import ResponseModel

class TokenService:

    def create_token(req_data, user_info):
        user_info["exp"] = datetime.utcnow() + timedelta(minutes=1)
        created_token = jwt.encode(user_info, Config.SECRET_KEY, Config.ALGORITHM)
        return ResponseModel.set_response(req_data.path, 200, "Done", created_token)

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

    def get_user_role(token):
        user_data = jwt.decode(token, Config.SECRET_KEY, Config.ALGORITHM)
        return user_data["role"]

    def get_user_approval(token):
        user_data = jwt.decode(token, Config.SECRET_KEY, Config.ALGORITHM)
        return user_data["approval"]

    def get_user(token):
        user_info = jwt.decode(token, Config.SECRET_KEY, Config.ALGORITHM)
        return user_info
