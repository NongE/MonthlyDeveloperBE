from functools import wraps
from flask import request

from service.token_service import TokenService


def validate_token_decorator(func):
    @wraps(func)
    def validste(*args, **kwargs):
        try:
            token = request.headers["Header"]
            if TokenService.validate_token(token):
                return func(*args, **kwargs)
            else:
                return {"result": "Unknown Header/Token"}
        except:
            return {"result": "Not Found Header/Token"}
    return validste