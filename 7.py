import utils
import base64
KEY = b"YELLOW SUBMARINE"

with open("7.txt", "r") as file:
	lines = file.readlines()
	
cipher = "".join([line[:-1] for line in lines])

plain = utils.AES_ECB_decrypt(KEY, base64.b64decode(cipher))

print(plain)