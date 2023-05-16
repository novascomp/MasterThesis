import os

from dotenv import load_dotenv
import time
load_dotenv('.env')
def write_hsm_config():
    with open('./cs_pkcs11_R3_template.cfg', 'r') as cfg_template, open('./cs_pkcs11_R3.cfg', 'a') as cfg_config:
        for line in cfg_template:
            cfg_config.write(line)
        HSM_SIMULATOR_PORT = os.environ.get('HSM_SIMULATOR_PORT')
        HSM_SIMULATOR_ADDRESS = os.environ.get('HSM_SIMULATOR_ADDRESS')
        cfg_config.write(f'Device={HSM_SIMULATOR_PORT}@{HSM_SIMULATOR_ADDRESS}')
write_hsm_config()
time.sleep(20)
from rest_api_module.rest_api import flask_app

if __name__ == '__main__':
    PORT = os.environ.get('PORT')
    HOST = os.environ.get('HOST')
    flask_app.run(host=HOST, port=PORT, debug=False)

# pipreqs --force to update requirements.txt
