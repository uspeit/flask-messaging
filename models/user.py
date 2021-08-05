import base64

from sqlalchemy import Column, Integer, String
from db import Base, db_session
from encryption import hash_password, encode_hash


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    def __init__(self, username=None, password=None, email=None):
        if not username or not password or not email:
            raise AttributeError
        self.username = username
        [salt_str, pass_hash_bytes] = hash_password(password)
        self.password_hash = "%s:%s" % (salt_str, encode_hash(pass_hash_bytes))
        self.email = email

    def save(self):
        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return '<User %r>' % self.username
