import logging

from pkcs11 import KeyType, Attribute, ObjectClass, lib

from rest_api_module.settings import PKCS11_MODULE, TOKEN_NAME, TOKEN_PASSWORD


def open_session(rw=True, user_pin=TOKEN_PASSWORD, token=lib(PKCS11_MODULE).get_token(token_label=TOKEN_NAME)):
    logging.info(f'PKCS #11 Session open')
    return token.open(rw, user_pin)


def get_key(session, key_label: str, key_length=256):
    logging.info(f'PKCS #11 Retrieving key')
    key = get_key_by_label(session, key_label)
    if key is None:
        return generate_aes_key(session, key_length, True, key_label)
    else:
        return key


def get_key_by_label(session, label):
    logging.info(f'PKCS #11 Get key by label')
    for obj in session.get_objects({
        Attribute.CLASS: ObjectClass.SECRET_KEY,
        Attribute.LABEL: label,
    }):
        return obj


def generate_aes_key(session, key_length: int, store: bool, label: str):
    logging.info(f'Generating AES key')
    return session.generate_key(KeyType.AES, key_length, store=store, label=label, template={
        Attribute.SENSITIVE: False,
        Attribute.EXTRACTABLE: False
    })


def encrypt_aes(key, data, iv):
    return key.encrypt(data, mechanism_param=iv)


def decrypt_aes(key, data, iv):
    return key.decrypt(data, mechanism_param=iv)
