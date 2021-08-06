from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, or_, and_
from auth import UnauthorizedError
from db import Base, db_session


class Message(Base):
    __tablename__ = 'messages'

    # Fields
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    message = Column(String, nullable=False)
    subject = Column(String(100), nullable=False)
    timestamp = Column(DateTime,
                       default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    # Flags
    read = Column(Boolean, default=False)
    sender_deleted = Column(Boolean, default=False)
    recipient_deleted = Column(Boolean, default=False)

    def __init__(self, sender_id=None, recipient_id=None, message=None, subject=None):
        if not sender_id or not recipient_id or not message or not subject:
            raise AttributeError
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.message = message
        self.subject = subject

    def save(self):
        db_session.add(self)
        db_session.commit()

    def to_dto(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "message": self.message,
            "subject": self.subject,
            "timestamp": self.timestamp.timestamp(),
        }

    def __repr__(self):
        return '<Message %d %s>' % (self.id, self.message)

    # DAO methods

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
