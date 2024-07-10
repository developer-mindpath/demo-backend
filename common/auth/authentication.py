import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from common.constants.common import UTF_8
from config import PRIVATE_KEY


def decrypt_message(encrypted_message):
    private_key = RSA.import_key(PRIVATE_KEY.encode(UTF_8))
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_bytes = base64.b64decode(encrypted_message)
    decrypted = cipher.decrypt(encrypted_bytes)
    return decrypted.decode(UTF_8)
