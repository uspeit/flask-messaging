from flask import Response, request
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
from auth import UnauthorizedError
from models.message import Message


class MessageApi(Resource):
    decorators = [jwt_required()]

    # -- GET /message
    # Return unread message
    @staticmethod
    def get():
        message = Message.read_one(current_identity.id)
        if message:
            return message.to_dto(), 200
        else:
            return {"error": "No unread messages"}, 404

    # -- DELETE /message/<message_id>
    # Remove message by id
    @staticmethod
    def delete(message_id=None):
        try:
            Message.remove(current_identity.id, message_id)
            return {"success": True}, 200
        except LookupError:
            return {"success": False, "error": "ID does not exist"}, 404
        except UnauthorizedError:
            return {"success": False, "error": "Unauthorized to alter this message"}, 401


class MessagesApi(Resource):
    decorators = [jwt_required()]

    # -- GET /messages/<all_or_unread>/<sent_or_received>
    # Return all/unread messages
    @staticmethod
    def get(all_or_unread="all", sent_or_received=None):
        include_read = all_or_unread == "all"
        include_sent = sent_or_received is None or sent_or_received == "sent"
        include_received = sent_or_received is None or sent_or_received == "received"
        # Get all messages sent/received by current user
        messages = Message.get_all(current_identity.id, include_read, include_sent, include_received)
        # Map Message list to json
        messages_json = list()
        for m in messages:
            messages_json.append(m.to_dto())
        return messages_json, 200

    # -- POST /messages
    # Add message to the collection
    @staticmethod
    def post():
        try:
            # Create message by current user with request body
            Message(current_identity.id, **request.get_json()).save()
            return {"success": True}, 200
        except AttributeError:
            return {
                       "success": False,
                       "error": "Invalid request body, Please provide a json with keys [recipient_id, message, subject]"
                   }, 400
