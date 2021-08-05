import os
from secrets import token_bytes

key = token_bytes(64)
key_dir = os.path.dirname(os.path.realpath(__file__)) + "/keys"
os.mkdir(key_dir)
key_file = open(key_dir + "/secret.txt", "wb")
key_file.write(key)
key_file.close()
