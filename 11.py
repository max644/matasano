import utils
from random import randint

BLOCKSIZE = 16

def encryption_oracle(plain):
	prefix = utils.randomString(randint(5, 10))
	suffix = utils.randomString(randint(5, 10))
	if randint(0, 1) == 0:
		return utils.AES_ECB_encrypt(utils.randomString(BLOCKSIZE), prefix + plain + suffix), "ECB"
	else:
		return utils.AES_CBC_encrypt(utils.randomString(BLOCKSIZE), utils.randomString(BLOCKSIZE), prefix + plain + suffix), "CBC"
	

for idx in range(10):
	cipher, method = encryption_oracle(b"A"*43)
	
	if cipher[BLOCKSIZE:BLOCKSIZE*2] == cipher[BLOCKSIZE*2:BLOCKSIZE*3]:
		methodGuess = "ECB"
	else:
		methodGuess = "CBC"
		
	print(methodGuess == method)
	