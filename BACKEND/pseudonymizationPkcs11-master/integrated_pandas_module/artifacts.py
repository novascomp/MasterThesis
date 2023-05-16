import binascii
from pkcs11_modul.service import encrypt_aes, decrypt_aes


class Crypto:
    def as_bytes(self):
        return binascii.unhexlify(self.hex_val)

    def as_hex_val(self):
        return binascii.hexlify(self.bytes).decode()


class IvCrypto(Crypto):
    def __init__(self, session, hex_value=None):
        if hex_value is None:
            self.bytes: bytes = session.generate_random(128)
            self.hex_val = self.as_hex_val()
        else:
            self.hex_val = hex_value
            self.bytes: bytes = self.as_bytes()


class EncryptedCrypto(Crypto):
    # https://stackoverflow.com/questions/43787031/python-byte-array-to-bit-array
    def __init__(self, key, record: str, iv: IvCrypto):
        self.iv: IvCrypto = iv
        self.bytes: bytes = encrypt_aes(key, str(record).encode(), self.iv.as_bytes())


class DecryptedCrypto(Crypto):
    def __init__(self, key, hex_val, iv: IvCrypto):
        self.iv: IvCrypto = iv
        self.hex_val = hex_val
        self.bytes: bytes = self.as_bytes()
        self.value = decrypt_aes(key, self.bytes, iv.as_bytes())
