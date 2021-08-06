import base64
import hashlib
from secrets import token_bytes


# Create PBKDF2 hash, returns salt, hash
def hash_password(password, salt_str=None):
    if not salt_str:
        # Generate unique salt
        salt_bytes = token_bytes(64)
        salt_str = bytes_to_b64_str(salt_bytes)
    else:
        # Decode provided salt string
        salt_bytes = b64_str_to_bytes(salt_str)
    pass_hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(), salt_bytes, 100000)
    return salt_str, pass_hash_bytes


def bytes_to_b64_str(bytes_in):
    return base64.b64encode(bytes_in).decode()


def b64_str_to_bytes(str_in):
    return base64.b64decode(str_in.encode())
