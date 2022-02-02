from config.config import Config
from app import create_env


if __name__ == '__main__':
    create_env().run(Config.HOST_IP, port=Config.PORT, debug=True)
