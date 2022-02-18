from flask import request
from functools import wraps

from service.token_service import TokenService
from model.response_model import ResponseModel


def token_validator(func):
    @wraps(func)
    def validate(*args, **kwargs):
        if "Header" in request.headers:
            token = request.headers["Header"]
            if TokenService.validate_token(token) and TokenService.get_user_approval(token):
                return func(*args, **kwargs)
            else:
                return ResponseModel.set_response(request.path, 200, "Unknown Header/Token", None)
        else:
            return ResponseModel.set_response(request.path, 200, "Not Found Header/Token", None)
    return validate
