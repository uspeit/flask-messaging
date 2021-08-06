from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
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
