import os

PKCS11_MODULE = os.environ['PKCS11_MODULE']
ENCODING = os.environ.get('ENCODING')
UPLOAD_ROOT = os.environ.get('UPLOAD_ROOT')
UPLOAD_DIR = os.environ.get('UPLOAD_DIR')
OUTPUT_DIR = os.environ.get('OUTPUT_DIR')
TOKEN_NAME = os.environ.get('TOKEN_NAME')
TOKEN_PASSWORD = os.environ.get('TOKEN_PASSWORD')
ISSUER = os.environ.get('ISSUER')
DB_FILE = os.environ.get('DB_FILE')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_FILE}'
NVF_ENDPOINT = os.environ.get('NVF_ENDPOINT')
NVF_ENDPOINT_NAMESPACE = os.environ.get('NVF_ENDPOINT_NAMESPACE')
HOSTING_ENDPOINT = os.environ.get('HOSTING_ENDPOINT')
CORS_LOCALHOST = os.environ.get('CORS_LOCALHOST')
CORS_HOSTING = os.environ.get('CORS_HOSTING')
CORS_GITHUB_HOSTING = os.environ.get('CORS_GITHUB_HOSTING')

# REDIS
STATIC_SALT = os.environ.get('STATIC_SALT')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_PORT = os.environ.get('REDIS_PORT')

# SPARK
SPARK_MASTER_HOST = os.environ.get('SPARK_MASTER_HOST')
SPARK_MASTER_PORT = os.environ.get('SPARK_MASTER_PORT')
SPARK_EXECUTOR_MEMORY = os.environ.get('SPARK_EXECUTOR_MEMORY')

NA_CHAR = os.environ.get('NA_CHAR')
HDFS_PATH = os.environ.get('HDFS_PATH')
OKTA_DISABLED = os.environ.get('OKTA_DISABLED')
