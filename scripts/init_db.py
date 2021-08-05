import os
from db import init_db, data_path

os.mkdir(data_path)
init_db()
