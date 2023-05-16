from enum import Enum

VERSION = "1.0"
PAGE_TITLE = "HSM (PKCS#11, CXI) and (REDIS) Demo"
PAGE_DESCRIPTION = "Python/Scala Demo app for pseudonymization"


class EncryptParserEnum(Enum):
    TECHNOLOGY = "technology"
    KEY_LABEL = "key_label"
    COL_NAMES_TO_PSEUD = "col_names_to_encrypt"
    FILE = "file"
    PSEUD_OPERATION_LABEL = "pseud_operation"


class UploadType(Enum):
    HTTPS = "https"
    HDFS = "hdfs"
    DIRECT = "direct"


class EncryptionStatus(Enum):
    IN_PROGRESS = "In progress"
    FAILED = "Failed"
    DONE = "Done"


class PseudType(Enum):
    ENCRYPT = "encrypt"
    HASH = "hash"


class PseudOperation(Enum):
    PSEUD = "pseud"
    DE_PSEUD = "de_pseud"


class EndpointTechnology(Enum):
    PYTHON_PANDAS_PKCS11_NONE = "python_pandas_pkcs11_none"
    PYTHON_SPARK_PKCS11_UDF = "python_spark_pkcs11_udf"
    PYTHON_SPARK_REDIS_UDF = "python_spark_redis_udf"
    PYTHON_SPARK_PKCS11_COLLECT = "python_spark_pkcs11_collect"
    PYTHON_SPARK_REDIS_COLLECT = "python_spark_redis_collect"
    SCALA_SPARK_CXI = "scala_spark_cxi_none"
    SCALA_SPARK_JCE = "scala_spark_jce_none"
    SCALA_SPARK_PKCS11 = "scala_spark_pkcs11_none"


class PseudOptions:
    def __init__(self, pseud_type: PseudType, operation: PseudOperation, technology: EndpointTechnology,
                 key_label: str):
        self.operation: PseudOperation = operation
        self.pseud_type: PseudType = pseud_type
        self.technology: EndpointTechnology = technology
        self.key_label: str = key_label
