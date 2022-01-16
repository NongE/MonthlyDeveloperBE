import os
from dotenv import load_dotenv

from app import create_env

load_dotenv()

if __name__ == '__main__':
    create_env().run(os.environ.get("HOST_IP"), port=os.environ.get("PORT, debug=True"))
