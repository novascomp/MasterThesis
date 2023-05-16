import os

import requests
from flask import request, Flask
from flask_cors import CORS
from flask_restx import Resource, fields, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from airport_info import AirportRecord
from ares import ARESRecord
from database.database_main import save_to_db
from generator import MAX_SAMPLE_SIZE, MIN_SAMPLE_SIZE, get_generated_data_file_name
from generator.gen_main import init_pool, generate_samples
from helpers import is_access_token_valid, parse_user_token
import logging

from settings import ENCODING

logging.basicConfig(filename='record.log', format='%(asctime)s %(message)s', level=logging.INFO)
flask_app = Flask(__name__)

flask_app.config.from_pyfile('settings.py')

with flask_app.app_context():
    db = SQLAlchemy(flask_app)


    class Mapping(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        uid = db.Column(db.String(50), nullable=False)
        file_id = db.Column(db.String(50), unique=True, nullable=False)
        location = db.Column(db.String(50), unique=True, nullable=False)


    if not os.path.isfile(f'instance/{flask_app.config.get("DB_FILE")}'):
        db.create_all()

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

app = Api(app=flask_app,
          version="1.0",
          title="Dat Gen App",
          description="Sample data generator",
          security='Bearer Auth',
          authorizations=authorizations)

v1 = app.namespace("v1", description='API v1')
flask_app.logger.info("POOL INIT")
flask_app.logger.info(f'ARES POOL: {flask_app.config.get("ARES_POOL")}')
flask_app.logger.info(f'AIRPORT INFO POOL: {flask_app.config.get("AIRPORT_INFO_POOL")}')
data_pool = init_pool(flask_app.config.get("ARES_POOL"), flask_app.config.get("AIRPORT_INFO_POOL"),
                      flask_app.config.get("RAPID_API_KEY"))
flask_app.logger.info("POOL INIT DONE")

# https://flask-restx.readthedocs.io/en/latest/_modules/flask_restx/fields.html
sample = app.model('sample', {
    'size': fields.Integer(required=True, description='Sample Size')
})

nvf_mapping = app.model('nvf_mapping', {
    'id': fields.Integer(required=True, description='Id'),
    'uid': fields.String(required=True, description='User Uid'),
    'file_id': fields.String(required=True, description='File Id'),
    'location': fields.String(required=True, description='Location')
})

CORS_LOCALHOST = flask_app.config.get("CORS_LOCALHOST")
CORS_HOSTING = flask_app.config.get("CORS_HOSTING")
CORS_GITHUB_HOSTING = flask_app.config.get("CORS_GITHUB_HOSTING")
cors = CORS(flask_app, resources={r"/v1/*": {"origins": [CORS_LOCALHOST, CORS_HOSTING, CORS_GITHUB_HOSTING]}})


@v1.route("/user")
@v1.header('Authorization: Bearer', 'JWT TOKEN', required=True)
class UserInfo(Resource):
    def get(self):
        if not is_authorized(request):
            unauthorized()

        return get_token_detail(request)


@v1.route("/user/files")
@v1.header('Authorization: Bearer', 'JWT TOKEN', required=True)
@v1.doc(params={'page_id': 'Page number', 'per_page': 'Records per page'})
class UserFiles(Resource):

    def get(self):
        if not is_authorized(request):
            unauthorized()
        uid = get_token_detail(request)["uid"]
        page_id = request.args.get('page_id', type=int)
        per_page = request.args.get('per_page', type=int)
        total_elements = Mapping.query.filter_by(uid=uid).count()
        return list(
            map(lambda x: {"id": x.id, "location": replace_hosting_domain(x.location),
                           "total_elements": total_elements},
                Mapping.query.filter_by(uid=uid).order_by(desc("id")).paginate(page=page_id, per_page=per_page)))


@v1.route("/genData")
@v1.header('Authorization: Bearer', 'JWT TOKEN', required=True)
class DataGen(Resource):

    @app.doc(responses={200: 'OK', 401: 'Unauthorized', 403: 'Bad Request'}, description="Data generator")
    @v1.expect(sample)
    def post(self):
        if not is_authorized(request):
            unauthorized()
        if check_input():
            sample_size = request.get_json()["size"]
            file_id = generate_samples(sample_size, data_pool)
            location = upload_file_to_storage(
                f'{flask_app.config.get("NVF_ENDPOINT")}{flask_app.config.get("NVF_ENDPOINT_NAMESPACE")}', file_id)
            uid = get_token_detail(request)["uid"]
            mapping = Mapping(uid=uid, file_id=file_id, location=location)
            save_to_db(db, mapping)
            return {"id": mapping.id, "location": replace_hosting_domain(location)}
        else:
            invalid_request()


@v1.route("/schema")
@v1.header('Authorization: Bearer', 'JWT TOKEN', required=True)
class UserFiles(Resource):

    def get(self):
        if not is_authorized(request):
            unauthorized()
        return {"schema": [ARESRecord.ICO, ARESRecord.FIRST_NAME, ARESRecord.LAST_NAME, ARESRecord.COMPANY,
                           ARESRecord.HEADQUARTERS, ARESRecord.DEGREE,
                           AirportRecord.PHONE, AirportRecord.LOCATION, AirportRecord.STREET, AirportRecord.CITY,
                           AirportRecord.COUNTRY, AirportRecord.POSTAL_CODE]}


def upload_file_to_storage(service_url, fileid) -> str:
    files = {'file': open(get_generated_data_file_name(fileid), 'r', encoding=ENCODING)}
    getdata = requests.post(service_url, files=files)
    print(getdata)
    return getdata.headers.get("Location")


def is_authorized(request):
    try:
        token = request.headers.get("Authorization").split("Bearer ")[1]
        return is_access_token_valid(token, flask_app.config.get("ISSUER"))
    except Exception:
        return False


def get_token_detail(request):
    token = request.headers.get("Authorization").split("Bearer ")[1]
    return parse_user_token(token, flask_app.config.get("ISSUER"))


def unauthorized():
    v1.abort(401, status="Unauthorized", statusCode="401")


def invalid_request():
    v1.abort(403, status="Bad Request", statusCode="403")


def check_input():
    try:
        sample_size = request.get_json()["size"]
        if MIN_SAMPLE_SIZE <= int(sample_size) <= MAX_SAMPLE_SIZE:
            logging.info(f'Requested sample_size: {sample_size}')
            return True
    except Exception:
        return False


def replace_hosting_domain(location):
    return location.replace(flask_app.config.get("NVF_ENDPOINT"), flask_app.config.get("HOSTING_ENDPOINT"))
