from sqlalchemy import Column, Integer, String
from db import Base, db_session
from hash import hash_password


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password_hash = hash_password(password)
        self.email = email

    def save(self):
        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return '<User %r>' % self.username
