from base64 import b64encode, b64decode
from zlib import compress, decompress


def encrypt_password(password):
    password = compress(password)
    password = b64encode(password)
    return password


def decrypt_password(encrypted_password):
    encrypted_password = b64decode(encrypted_password)
    encrypted_password = decompress(encrypted_password)
    return encrypted_password
