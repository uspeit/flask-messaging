import hashlib
salt = 'test'.encode('utf-8')


def hash_password(password):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
