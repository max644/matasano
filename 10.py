import utils

KEY = b"YELLOW SUBMARINE"
BLOCKSIZE = 16

with open("10.txt", "r") as file:
	lines = file.readlines()
	
cipher = "".join([line[:-1] for line in lines])

plain = utils.AES_CBC_decrypt(KEY, b"\x00"*BLOCKSIZE, utils.b64Decode(cipher))

print(plain)