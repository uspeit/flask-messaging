import json
from json.decoder import JSONDecodeError
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from dao.user import UserDao
from entities.user import User


class RegisterApi(Resource):
    @staticmethod
    def post():
        try:
            body = json.loads(request.data, strict=False)
            User(**body).save()
            user = UserDao.get_by_username(username=body['username'])
            return {"success": True, "id": user.id}, 200
        except JSONDecodeError:
            return {
                       "success": False,
                       "message": "Unable to parse request. Unexpected JSON format"
                   }, 400
        except AttributeError:
            return {
                       "success": False,
                       "message": "Incorrect body, please provide [username, password, email] as a json body"
                   }, 400
        except IntegrityError:
            return {"success": False, "message": "Username or Email already exist"}, 400
