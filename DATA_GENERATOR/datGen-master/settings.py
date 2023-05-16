import os

DB_FILE = os.environ.get('DB_FILE')
NVF_ENDPOINT = os.environ.get('NVF_ENDPOINT')
NVF_ENDPOINT_NAMESPACE = os.environ.get('NVF_ENDPOINT_NAMESPACE')
HOSTING_ENDPOINT = os.environ.get('HOSTING_ENDPOINT')
ARES_POOL = int(os.environ.get('ARES_POOL'))
AIRPORT_INFO_POOL = int(os.environ.get('AIRPORT_INFO_POOL'))
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE}'
RAPID_API_KEY = os.environ.get('RAPID_API_KEY')
ISSUER = os.environ.get('ISSUER')
ENCODING = os.environ.get('ENCODING')
CORS_LOCALHOST = os.environ.get('CORS_LOCALHOST')
CORS_HOSTING = os.environ.get('CORS_HOSTING')
CORS_GITHUB_HOSTING = os.environ.get('CORS_GITHUB_HOSTING')