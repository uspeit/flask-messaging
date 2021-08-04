from werkzeug.security import hmac

from hash import hash_password
from models.user import User


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    password_hash = hash_password(password)
    if user and hmac.compare_digest(user.password_hash, password_hash):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()
