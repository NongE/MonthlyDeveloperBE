from flask import Blueprint, url_for
from authlib.integrations.flask_client import OAuth
from config.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
oauth = OAuth()

auth = Blueprint('auth', __name__)

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
@auth.route('/login/github')
def github_login():
    github_ = oauth.create_client('github')
    redirect_uri = url_for('auth.github_authorize', _external=True)
    return github_.authorize_redirect(redirect_uri)


# Github authorize route
@auth.route('/login/github/authorize')
def github_authorize():

    # github_ = oauth.create_client('github')
    # access_token = github_.authorize_access_token()['access_token']
    # 위와 같은 식으로도 사용 가능

    access_token = oauth.github.authorize_access_token()['access_token']
    resp = oauth.github.get('user').json()

    user_ID, email = resp['login'], resp['email']

    return f"You are successfully signed in using github, user_ID : {user_ID} / E-mail : {email}"
