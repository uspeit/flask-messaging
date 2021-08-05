import base64
import hashlib
from secrets import token_bytes


# Create PBKDF2 hash, returns salt, hash
def hash_password(password, salt_str=None):
    if not salt_str:
        # Generate unique salt
        salt_bytes = token_bytes(64)
        salt_str = base64.b64encode(salt_bytes).decode('unicode_escape')
    else:
        # Decode provided salt string
        salt_bytes = base64.b64decode(salt_str.encode('unicode_escape'))
    pass_hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode('unicode_escape'), salt_bytes, 100000)
    return salt_str, pass_hash_bytes


def encode_hash(hash_bytes):
    return base64.b64encode(hash_bytes).decode('unicode_escape')
