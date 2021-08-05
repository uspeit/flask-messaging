import json
from flask import Response, request
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource
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


class MessagesApi(Resource):
    decorators = [jwt_required()]

    # -- GET /messages/<type>
    # Return all/unread messages
    def get(self, message_type="all"):
        if message_type == "all":
            return self.get_messages(False)
        if message_type == "unread":
            return self.get_messages(True)
        return {
            "success": False,
            "error": "Invalid endpoint, please use /messages/all or /messages/unread"
        }, 400

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
                "error": "Invalid request body, please provide json with [sender_id, recipient_id, message, subject]"
            }, 400

    # Helper methods

    @staticmethod
    def get_messages(unread=False):
        # Get all messages sent/received by current user
        messages = Message.get_all(current_identity.id, unread)
        # Map Message list to json
        messages_json = list()
        for m in messages:
            messages_json.append(m.to_dto())
        return messages_json, 200