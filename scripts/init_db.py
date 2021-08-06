import os
from models.message import Message
from models.user import User
from db import Base, engine, data_path

os.mkdir(data_path)
Base.metadata.create_all(bind=engine)
