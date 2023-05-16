import logging
import os
import uuid

from sqlalchemy import desc

from flask import request, Flask
from flask_cors import CORS
from flask_restx import Api, Resource, reqparse, fields
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage

import integrated_spark_module_collect
from integrated_pandas_module.service import pandas_pkcs11_service
from helpers import is_access_token_valid, parse_user_token
from artifacts import Commander, GeneralModuleResponse
from rest_api_module import EncryptParserEnum, EncryptionStatus, VERSION, PAGE_TITLE, PAGE_DESCRIPTION, \
    EndpointTechnology, PseudOperation, UploadType
from rest_api_module.service import executor, pseud_locations_dict, upload_file_to_storage, get_pseud_options, \
    get_commander

from database.database_main import save_to_db
from rest_api_module.service import encryption_source_locations_dict
from rest_api_module.settings import NVF_ENDPOINT, NVF_ENDPOINT_NAMESPACE, HDFS_PATH, OKTA_DISABLED
from standalone_caller_spark_module.service import spark_service
from integrated_spark_module_collect.service import spark_service_collect

logging.basicConfig(filename='record.log', format='%(asctime)s %(message)s', level=logging.INFO)
flask_app = Flask(__name__)
flask_app.config.from_pyfile('settings.py')

with flask_app.app_context():
    db = SQLAlchemy(flask_app)


    class EncryptionMapping(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        uid = db.Column(db.String(50), nullable=False)
        request_id = db.Column(db.String(50), unique=True, nullable=False)
        source_location = db.Column(db.String(200), unique=False, nullable=False)
        encryption_location = db.Column(db.String(200), unique=False, nullable=True)
        technology = db.Column(db.String(50), unique=False, nullable=False)
        pseud_operation = db.Column(db.String(50), unique=False, nullable=False)
        key_label = db.Column(db.String(50), unique=False, nullable=False)
        status = db.Column(db.String(50), unique=False, nullable=False)
        date = db.Column(db.Date, unique=False, nullable=True)
        start = db.Column(db.Integer, unique=False, nullable=True)
        end = db.Column(db.Integer, unique=False, nullable=True)


    if not os.path.isfile(f'instance/{flask_app.config.get("DB_FILE")}'):
        db.create_all()

UPLOAD_PATH = f'{flask_app.config.get("UPLOAD_ROOT")}{flask_app.config.get("UPLOAD_DIR")}/'
OUTPUT_PATH = f'{flask_app.config.get("UPLOAD_ROOT")}{flask_app.config.get("OUTPUT_DIR")}/'

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

app = Api(app=flask_app,
          version=VERSION,
          title=PAGE_TITLE,
          description=PAGE_DESCRIPTION,
          security='Bearer Auth',
          authorizations=authorizations)

v1 = app.namespace("v1", description='PKCS#11 Crypto API')

direct_parser = reqparse.RequestParser()
direct_parser.add_argument(EncryptParserEnum.TECHNOLOGY.value, type=str, required=True,
                           default=EndpointTechnology.PYTHON_PANDAS_PKCS11_NONE.value)
direct_parser.add_argument(EncryptParserEnum.PSEUD_OPERATION_LABEL.value, type=str, required=True,
                           default=PseudOperation.PSEUD.value)
direct_parser.add_argument(EncryptParserEnum.KEY_LABEL.value, type=str, required=False, default='test')
direct_parser.add_argument(EncryptParserEnum.COL_NAMES_TO_PSEUD.value, type=str, required=True, action='append')
direct_parser.add_argument(EncryptParserEnum.FILE.value, location='files', type=FileStorage, required=True)

hdfs_parser = reqparse.RequestParser()
hdfs_parser.add_argument(EncryptParserEnum.TECHNOLOGY.value, type=str, required=True,
                         default=EndpointTechnology.PYTHON_SPARK_PKCS11_UDF.value)
hdfs_parser.add_argument(EncryptParserEnum.PSEUD_OPERATION_LABEL.value, type=str, required=True,
                         default=PseudOperation.PSEUD.value)
hdfs_parser.add_argument(EncryptParserEnum.KEY_LABEL.value, type=str, required=False, default='test')
hdfs_parser.add_argument(EncryptParserEnum.COL_NAMES_TO_PSEUD.value, type=str, required=True, action='append')
hdfs_parser.add_argument(EncryptParserEnum.FILE.value, type=str, required=True, default='test.csv')

file_location = app.model('file_location', {
    EncryptParserEnum.KEY_LABEL.value: fields.String(default="test", required=False, description='Key label'),
    EncryptParserEnum.TECHNOLOGY.value: fields.String(default=EndpointTechnology.PYTHON_PANDAS_PKCS11_NONE.value,
                                                      required=False,
                                                      description='Technology'),
    EncryptParserEnum.PSEUD_OPERATION_LABEL.value: fields.String(default=PseudOperation.PSEUD.value, required=False,
                                                                 description='Technology'),
    EncryptParserEnum.COL_NAMES_TO_PSEUD.value: fields.List(fields.String(default="id"), required=True),
    EncryptParserEnum.FILE.value: fields.String(default="https://nvf", required=True, description='File location')
})

CORS_LOCALHOST = flask_app.config.get("CORS_LOCALHOST")
CORS_HOSTING = flask_app.config.get("CORS_HOSTING")
CORS_GITHUB_HOSTING = flask_app.config.get("CORS_GITHUB_HOSTING")
cors = CORS(flask_app, resources={r"/v1/*": {"origins": [CORS_LOCALHOST, CORS_HOSTING, CORS_GITHUB_HOSTING]}})


@v1.route("/pseud")
class Pseud(Resource):

    @app.doc(responses={202: 'Accepted'}, description="Spark module supporting PKCS#11 and REDIS")
    @v1.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @app.expect(direct_parser)
    def post(self):
        if not is_authorized(request):
            unauthorized()

        request_id = uuid.uuid4().hex
        logging.info(f'Direct ENDPOINT, INIT Request ID: {request_id}')
        args = direct_parser.parse_args()
        send_to_desired_module(args, request_id, UploadType.DIRECT)
        return {"request_id": request_id}, 202


@v1.route("/pseud/hdfs")
class Pseud_hdfs(Resource):

    @app.doc(responses={202: 'Accepted'}, description="HDFS Cluster")
    @v1.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @app.expect(hdfs_parser)
    def post(self):
        if not is_authorized(request):
            unauthorized()

        request_id = uuid.uuid4().hex
        logging.info(f'HDFS ENDPOINT, INIT Request ID: {request_id}')
        args = hdfs_parser.parse_args()
        send_to_desired_module(args, request_id, UploadType.HDFS)
        return {"request_id": request_id}, 202


@v1.route("/pseud/https")
class Pseud_https(Resource):

    @app.doc(responses={202: 'Accepted'}, description="Download file from HTTP/HTTPS")
    @v1.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @app.expect(file_location)
    def post(self):
        if not is_authorized(request):
            unauthorized()

        direct = False
        request_id = uuid.uuid4().hex
        logging.info(f'Https ENDPOINT, INIT Request ID: {request_id}')
        args = dict()

        args[EncryptParserEnum.FILE.value] = request.get_json()[EncryptParserEnum.FILE.value]
        args[EncryptParserEnum.KEY_LABEL.value] = request.get_json()[EncryptParserEnum.KEY_LABEL.value]
        args[EncryptParserEnum.COL_NAMES_TO_PSEUD.value] = request.get_json()[
            EncryptParserEnum.COL_NAMES_TO_PSEUD.value]

        args[EncryptParserEnum.TECHNOLOGY.value] = request.get_json()[EncryptParserEnum.TECHNOLOGY.value]
        args[EncryptParserEnum.PSEUD_OPERATION_LABEL.value] = request.get_json()[
            EncryptParserEnum.PSEUD_OPERATION_LABEL.value]

        send_to_desired_module(args, request_id, UploadType.HTTPS)
        return {"request_id": request_id}, 202


@v1.route("/pseud/<string:request_id>")
class EncryptProcessStatus(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'Unauthorized', 404: 'NotFound'},
             description="Get encryption status")
    @v1.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    def get(self, request_id):
        if not is_authorized(request):
            unauthorized()

        uid = get_token_detail(request)["uid"]

        if EncryptionMapping.query.filter_by(uid=uid, request_id=request_id).count() == 0:
            not_found()

        return list(
            map(lambda record: {"id": record.id, "key_label": record.key_label.replace(f'{uid}_', '', 1),
                                "encryption_location": record.encryption_location,
                                "source_location": record.source_location,
                                "technology": record.technology,
                                "pseud_operation": record.pseud_operation,
                                "status": record.status,
                                "start": record.start,
                                "end": record.end
                                },
                EncryptionMapping.query.filter_by(uid=uid, request_id=request_id)))


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
        total_elements = EncryptionMapping.query.filter_by(uid=uid).count()
        return list(
            map(lambda record: {"id": record.id, "key_label": record.key_label.replace(f'{uid}_', '', 1),
                                "encryption_location": replace_hosting_domain(record.encryption_location),
                                "source_location": record.source_location,
                                "technology": record.technology,
                                "pseud_operation": record.pseud_operation,
                                "status": record.status,
                                "total_elements": total_elements,
                                "start": record.start,
                                "end": record.end
                                },
                EncryptionMapping.query.filter_by(uid=uid).order_by(desc("id")).paginate(page=page_id,
                                                                                         per_page=per_page)))


@v1.route("/user")
@v1.header('Authorization: Bearer', 'JWT TOKEN', required=True)
class UserInfo(Resource):
    def get(self):
        if not is_authorized(request):
            unauthorized()

        return get_token_detail(request)


def is_authorized(request):
    try:
        if OKTA_DISABLED == 'yes':
            return True
        token = request.headers.get("Authorization").split("Bearer ")[1]
        return is_access_token_valid(token, flask_app.config.get("ISSUER"))
    except Exception:
        return False


def unauthorized():
    v1.abort(401, status="Unauthorized", statusCode="401")


def not_found():
    v1.abort(404, status="NotFound", statusCode="404")


def get_token_detail(request):
    if OKTA_DISABLED == "yes":
        return {"uid": "randomUIDforrandomUser"}
    token = request.headers.get("Authorization").split("Bearer ")[1]
    return parse_user_token(token, flask_app.config.get("ISSUER"))


def send_to_desired_module(args, request_id, upload_type: UploadType):
    technology = args[EncryptParserEnum.TECHNOLOGY.value]
    pseud_operation = args[EncryptParserEnum.PSEUD_OPERATION_LABEL.value]
    uid = get_token_detail(request)["uid"]
    logging.info(f'Technology, operation, uid: {technology}, {pseud_operation}, {uid}')

    if technology == EndpointTechnology.PYTHON_SPARK_PKCS11_UDF.value or technology == EndpointTechnology.PYTHON_SPARK_PKCS11_COLLECT.value or technology == EndpointTechnology.PYTHON_PANDAS_PKCS11_NONE.value or technology == EndpointTechnology.SCALA_SPARK_CXI.value or technology == EndpointTechnology.SCALA_SPARK_JCE.value or technology == EndpointTechnology.SCALA_SPARK_PKCS11.value:
        key_label = f'{uid}_{args[EncryptParserEnum.KEY_LABEL.value]}'
        pseud_options = get_pseud_options(technology, pseud_operation, key_label)

        if technology == EndpointTechnology.PYTHON_SPARK_PKCS11_UDF.value or technology == EndpointTechnology.PYTHON_SPARK_PKCS11_COLLECT.value or technology == EndpointTechnology.SCALA_SPARK_CXI.value  or technology == EndpointTechnology.SCALA_SPARK_JCE.value or technology == EndpointTechnology.SCALA_SPARK_PKCS11.value:
            if upload_type == upload_type.HDFS:
                commander = get_commander(args, request_id, pseud_options, HDFS_PATH, upload_type)
                executor.submit(run_commander_spark, request_id, commander, uid, upload_type)
            else:
                commander = get_commander(args, request_id, pseud_options, UPLOAD_PATH, upload_type)
                executor.submit(run_commander_spark, request_id, commander, uid, upload_type)

        if technology == EndpointTechnology.PYTHON_PANDAS_PKCS11_NONE.value:
            commander = get_commander(args, request_id, pseud_options, UPLOAD_PATH, upload_type)
            executor.submit(run_pandas_pkcs11, request_id, commander, uid, upload_type)

    if technology == EndpointTechnology.PYTHON_SPARK_REDIS_UDF.value or technology == EndpointTechnology.PYTHON_SPARK_REDIS_COLLECT.value:
        pseud_options = get_pseud_options(technology, pseud_operation)
        commander = get_commander(args, request_id, pseud_options, UPLOAD_PATH, upload_type)
        executor.submit(run_commander_spark, request_id, commander, uid, upload_type)


def run_commander_spark(request_id, commander: Commander, uid, upload_type: UploadType):
    response: GeneralModuleResponse = None
    update_request_in_db(uid, request_id, EncryptionStatus.IN_PROGRESS, commander, response)
    technology = commander.pseud_options.technology

    if technology == technology.PYTHON_SPARK_PKCS11_COLLECT or technology == technology.PYTHON_SPARK_REDIS_COLLECT:
        future = executor.submit(spark_service_collect, commander, upload_type)
    else:
        future = executor.submit(spark_service, commander, upload_type)

    try:
        response = future.result()
        if response is None:
            status = EncryptionStatus.FAILED
        else:
            status = EncryptionStatus.DONE

            if upload_type == upload_type.DIRECT or upload_type == upload_type.HTTPS:
                pseud_locations_dict[request_id] = upload_file_to_storage(f'{NVF_ENDPOINT}{NVF_ENDPOINT_NAMESPACE}',
                                                                          response.result_path)
            else:
                pseud_locations_dict[request_id] = response.result_path
    except Exception:
        status = EncryptionStatus.FAILED
        logging.exception()

    set_status(uid, request_id, status, commander, upload_type, response)


def run_pandas_pkcs11(request_id, commander, uid, upload_type: UploadType):
    response: GeneralModuleResponse = None
    update_request_in_db(uid, request_id, EncryptionStatus.IN_PROGRESS, commander, response)
    future = executor.submit(pandas_pkcs11_service, commander, OUTPUT_PATH)
    try:
        response = future.result()
        status = EncryptionStatus.DONE
        pseud_locations_dict[request_id] = upload_file_to_storage(f'{NVF_ENDPOINT}{NVF_ENDPOINT_NAMESPACE}',
                                                                  response.result_path)
    except Exception:
        status = EncryptionStatus.FAILED
        logging.exception(request_id)

    set_status(uid, request_id, status, commander, upload_type, response)


def set_status(uid, request_id, status, commander: Commander, upload_type: UploadType, response):
    # remove_uploaded_file(request_id, upload_path)
    update_request_in_db(uid, request_id, status, commander, response)


def update_request_in_db(uid, request_id, status, commander: Commander, response):
    pseud_location = pseud_locations_dict[request_id]
    source_location = encryption_source_locations_dict[request_id]
    if status == EncryptionStatus.IN_PROGRESS:
        technology = commander.pseud_options.technology
        key_label = commander.pseud_options.key_label
        pseud_operation = commander.pseud_options.operation
        logging.info(
            f'{uid}, {request_id}, {pseud_location}, {source_location}, {status.value}, {technology}, {key_label}')
        mapping = EncryptionMapping(uid=uid, request_id=request_id, source_location=source_location,
                                    technology=technology.value, pseud_operation=pseud_operation.value,
                                    key_label=key_label,
                                    status=status.value)

        with flask_app.app_context():
            save_to_db(db, mapping)
    else:
        with flask_app.app_context():
            mapping = EncryptionMapping.query.filter_by(uid=uid, request_id=request_id).first()
            mapping.encryption_location = pseud_location
            mapping.status = status.value
            if response is not None:
                mapping.start = int(response.start_time)
                mapping.end = int(response.end_time)
            db.session.commit()


def replace_hosting_domain(location):
    if location is not None:
        return location.replace(flask_app.config.get("NVF_ENDPOINT"), flask_app.config.get("HOSTING_ENDPOINT"))
    return location
