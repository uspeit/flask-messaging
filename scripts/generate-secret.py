from secrets import token_bytes

key = token_bytes(64)
key_file = open("../keys/secret.txt", "wb")
key_file.write(key)
key_file.close()
