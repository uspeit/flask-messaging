import os
from secrets import token_bytes

key = token_bytes(64)
key_file = open(os.path.dirname(os.path.realpath(__file__)) + "/keys/secret.txt", "wb")
key_file.write(key)
key_file.close()
