from flask_restx import fields, Namespace, reqparse


class AuthenticationModel():
    auth_ns = Namespace("Github Oauth", description="Github Oauth 로그인")

    github_access_code_parser = auth_ns.parser()
    github_access_code_parser.add_argument('code')

    create_jwt_model = auth_ns.model('create jwt model', {
        'login': fields.String(description='github login', required=True),
        'email': fields.String(description='github email', required=True),
    })

    validate_jwt = auth_ns.parser()
    validate_jwt.add_argument('header', location='headers')
