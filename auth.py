from werkzeug.security import hmac

from encryption import hash_password, encode_hash
from models.user import User


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        # Obtain user hash and user salt
        [user_salt, user_hash] = user.password_hash.split(":")
        # Hash password candidate with user salt
        [_, pass_hash_bytes] = hash_password(password, user_salt)
        pass_hash = encode_hash(pass_hash_bytes)
        # Compare hash digests
        if hmac.compare_digest(user_hash, pass_hash):
            return user


def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()
