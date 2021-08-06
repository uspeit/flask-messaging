from sqlalchemy import or_, and_
from auth import UnauthorizedError
from db import Base, db_session
from entities.message import Message


class MessageDao(Base):
    @staticmethod
    def read_one(user_id=None):
        # Find oldest unread
        message = Message.query.filter_by(recipient_id=user_id, read=False) \
            .order_by(Message.timestamp) \
            .first()
        # Mark as read
        if message:
            message.read = True
            message.save()
        return message

    @staticmethod
    def get_all(user_id=None, include_read=True, include_sent=True, include_received=True):
        received_filter = and_(Message.recipient_id == user_id, Message.recipient_deleted == False)
        sent_filter = and_(Message.sender_id == user_id, Message.sender_deleted == False)
        # Create filter combination
        if include_sent and include_received:
            query_filter = or_(received_filter, sent_filter)
        elif include_sent:
            query_filter = sent_filter
        elif include_received:
            query_filter = received_filter
        else:
            return []
        query = Message.query.filter(query_filter)
        # Filter unread if required
        if not include_read:
            query = query.filter_by(read=False)  # We do not mark messages as read when received in bulk
        return query.all()

    @staticmethod
    def remove(user_id=None, message_id=False):
        # Find message
        message = Message.query.filter_by(id=message_id).first()
        if not message:
            raise LookupError
        # Mark as deleted by user
        if message.sender_id == user_id:
            if message.sender_deleted:
                raise LookupError  # Message already deleted
            message.sender_deleted = True
        if message.recipient_id == user_id:
            if message.recipient_deleted:
                raise LookupError  # Message already deleted
            message.recipient_deleted = True
        # User was unauthorized if nothing changed
        if not message.sender_deleted and not message.recipient_deleted:
            raise UnauthorizedError
        if message.sender_deleted and message.recipient_deleted:
            # Both parties removed the message, remove from DB
            db_session.delete(message)
            db_session.commit()
        else:
            message.save()
