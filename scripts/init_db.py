import os
from models.message import Message
from models.user import User
from db import init_db, data_path

os.mkdir(data_path)
init_db()
