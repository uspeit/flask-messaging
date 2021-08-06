import os
from entities.message import Message
from entities.user import User
from db import Base, engine, data_path

os.mkdir(data_path)
Base.metadata.create_all(bind=engine)
