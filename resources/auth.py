import json
from flask import request
from flask_restful import Resource
from models.user import User

#
# class LoginApi(Resource):
#     def post(self):
#         body = request.get_json()
#         user = User(**body).save()
#         id = movie.id
#         return {'id': str(id)}, 200


class RegisterApi(Resource):
    def post(self):
        body = json.loads(request.data, strict=False)
        User(**body).save()
        user = User.query.filter_by(username=body['username']).first()
        return {'id': str(user.id)}, 200
