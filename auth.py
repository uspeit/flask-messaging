from werkzeug.security import hmac
from dao.user import UserDao
from encryption import hash_password, bytes_to_b64_str


class UnauthorizedError(BaseException):  # Exception for unauthorized actions
    pass


def authenticate(username, password):
    user = UserDao.get_by_username(username)
    if user:
        # Obtain user hash and user salt
        [user_salt, user_hash] = user.password_hash.split(":")
        # Hash password candidate with user salt
        [_, pass_hash_bytes] = hash_password(password, user_salt)
        pass_hash = bytes_to_b64_str(pass_hash_bytes)
        # Compare hash digests
        if hmac.compare_digest(user_hash, pass_hash):
            return user


def identity(payload):
    return UserDao.get_by_id(payload['identity'])
