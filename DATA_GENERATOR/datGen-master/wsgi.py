import os

from dotenv import load_dotenv
load_dotenv('.env')
from app import flask_app

if __name__ == '__main__':
    PORT = os.environ.get('PORT')
    HOST = os.environ.get('HOST')
    flask_app.run(host=HOST, port=PORT, debug=False)

# pipreqs --force to update requirements.txt
