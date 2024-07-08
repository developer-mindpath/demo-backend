from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import base64

def load_public_key():
    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key

def encrypt_message(message: str, public_key):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    encrypted_base64 = base64.b64encode(encrypted).decode('utf-8')
    return encrypted_base64

print(encrypt_message("string",load_public_key()))

{
  "first_name": "Josh",
  "last_name": "Buttler",
  "email": "josh@gmail.com",
  "password": "josh@123"
}