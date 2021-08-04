import json
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from db import Base, db_session


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('user.id'))
    recipient_id = Column(Integer, ForeignKey('user.id'))
    message = Column(String)
    subject = Column(String(100))
    timestamp = Column(DateTime,
                       default=datetime.utcnow,
                       onupdate=datetime.utcnow)

    def __init__(self, sender_id=None, recipient_id=None, message=None, subject=None):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.message = message
        self.subject = subject

    def save(self):
        db_session.add(self)
        db_session.commit()

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "message": self.message,
            "subject": self.subject,
            "timestamp": self.timestamp.timestamp(),
        })

    def __repr__(self):
        return '<Message %r %r>' % self.id % self.message
