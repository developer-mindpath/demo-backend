from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import base64

PUBLIC_KEY_PATH = "./public_key.pem"
PRIVATE_KEY_PATH = "./private_key.pem"

def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def decrypt_message(encrypted_message, private_key):
    encrypted_message = base64.b64decode(encrypted_message.encode('utf-8'))
    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return decrypted.decode()

private_key = load_private_key()
public_key = load_public_key()
