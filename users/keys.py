import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from users.config import PRIVATE_KEY


def decrypt_message(encrypted_message):
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=None)
    encrypted_bytes = base64.b64decode(encrypted_message.encode('utf-8'))
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return decrypted.decode('utf-8')
