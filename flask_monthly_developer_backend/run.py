from app import create_env
from config.env import Env

if __name__ == '__main__':
    create_env().run(Env.HOST_IP, port=Env.PORT, debug=True)