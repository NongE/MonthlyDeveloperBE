from flask import url_for
from flask_restx import Resource, Namespace
from authlib.integrations.flask_client import OAuth
from config.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

oauth = OAuth()

auth_ns = Namespace("Github Oauth", description="Github Oauth 로그인")

github = oauth.register(
    name='github',
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# Github login route
@auth_ns.route('/github', methods=['GET'])
class GithubLogin(Resource):
    def get(self):
        github_ = oauth.create_client('github')
        redirect_uri = url_for('Github Oauth_github_authorize', _external=True)
        return github_.authorize_redirect(redirect_uri)


# Github authorize route
@auth_ns.route('/github/authorize', methods=['GET'])
class GithubAuthorize(Resource):
    def get(self):

        # github_ = oauth.create_client('github')
        # access_token = github_.authorize_access_token()['access_token']
        # 위와 같은 식으로도 사용 가능

        access_token = oauth.github.authorize_access_token()['access_token']
        resp = oauth.github.get('user').json()

        user_ID, email = resp['login'], resp['email']

        return f"You are successfully signed in using github, user_ID : {user_ID} / E-mail : {email}"
