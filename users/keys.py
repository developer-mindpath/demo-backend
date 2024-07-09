import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from users.config import PRIVATE_KEY


def decrypt_message(encrypted_message):
    private_key = RSA.import_key(PRIVATE_KEY.encode('utf-8'))
    cipher = PKCS1_OAEP.new(private_key)
    encrypted_bytes = base64.b64decode(encrypted_message)
    decrypted = cipher.decrypt(encrypted_bytes)
    return decrypted.decode('utf-8')
