from functools import wraps
from flask import request

from service.token_service import TokenService
from model import response_model

response_model = response_model.ResponseModel()


def validate_token_decorator(func):
    @wraps(func)
    def validate(*args, **kwargs):
        try:
            token = request.headers["Header"]
            if TokenService.validate_token(token):
                return func(*args, **kwargs)
            else:
                return response_model.set_response(request.path, 200, "Unknown Header/Token", None)
        except:
            return response_model.set_response(request.path, 200, "Not Found Header/Token", None)
    return validate