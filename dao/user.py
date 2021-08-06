from db import db_session
from entities.user import User


class UserDao:
    @staticmethod
    def add_user(username=None, password=None, email=None):
        db_session.add(User(username, password, email))
        db_session.commit()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_id(user_id):
        return User.query.filter_by(id=user_id).first()
