import json
from flask import Response, request
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from models.message import Message


class MessagesApi(Resource):
    decorators = [jwt_required()]

    def get(self):
        messages = Message.query.filter_by(sender_id=current_identity.id).all()
        messages_json = list()  # Map Message objects to json strings
        for m in messages:
            messages_json.append(m.to_json())
        response = "[%s]" % ','.join(messages_json) # Create json list
        return Response(response, mimetype="application/json", status=200)

    def post(self):
        sender_id = current_identity.id
        body = request.get_json()
        message = Message(sender_id, **body).save()
        return Response(message, mimetype="application/json", status=200)
