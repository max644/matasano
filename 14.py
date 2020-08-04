import utils
from random import randint

BLOCKSIZE = 32 if randint(1,2) == 1 else 16
KEY = utils.randomString(BLOCKSIZE)
PREFIX = utils.randomString(randint(50, 100))

SECRET_PLAIN_STR = utils.b64Decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")

def encryption_oracle(plain):
	#print "message : " + (PREFIX + plain + SECRET_PLAIN_STR)[0:16]
	return utils.AES_ECB_encrypt(KEY, PREFIX + plain + SECRET_PLAIN_STR)
	
# print "PREFIX length : " + str(len(PREFIX))
# print "SUFFIX length : " + str(len(SECRET_PLAIN_STR))
# print "cipher length : " + str(len(utils.AES_ECB_encrypt(KEY, PREFIX + SECRET_PLAIN_STR)))
# print "padding length : " + str(len(utils.AES_ECB_encrypt(KEY, PREFIX + SECRET_PLAIN_STR)) - len(PREFIX + SECRET_PLAIN_STR))
# print "SECRET_PLAIN_STR length : " + str(len(SECRET_PLAIN_STR))
# -------------------------------------------------------------------------
	
def getBlockById(cipher, blockId, blocksize):
	return cipher[blocksize*blockId:blocksize*(blockId+1)]
	
def getBlockSize():
	initLen = len(encryption_oracle(b"A"))
	cipherSize = 1
	curCipherSize = initLen
	while curCipherSize == initLen:
		cipherSize += 1
		curCipherSize = len(encryption_oracle(b"A"*cipherSize))
	return curCipherSize - initLen

def getFirstDifferentBlockId(cipherA, cipherB, blocksize):
	idx = 0
	while getBlockById(cipherA, idx, blocksize) == getBlockById(cipherB, idx, blocksize):
		idx += 1
	return idx
	
def getCipherInfos(blocksize):
	# compute prefix block number & suffix block number
	cipherA = encryption_oracle(b"")
	cipherB = encryption_oracle(b"B")
	idx = getFirstDifferentBlockId(cipherA, cipherB, blocksize)
	prefixLength = idx * blocksize
	suffixLength = len(cipherA) - ((idx + 1) * blocksize)
	
	# compute last block (shared with prefix and suffix) bytes of prefix / bytes of suffix
	cursor = 0
	while getBlockById(encryption_oracle(b"A" * (cursor+1)), idx+1, blocksize) == getBlockById(encryption_oracle(b"B" * (cursor+1)), idx+1, blocksize):
		cursor += 1
	prefixLength += blocksize - cursor
	suffixLength += cursor
	
	# compute trailling padding
	padding = 0
	while len(encryption_oracle(b"A" * (padding+1))) == len(cipherA):
		padding += 1
	suffixLength -= (padding % blocksize) + 1
	
	return prefixLength, suffixLength

def isAES_ECB(blocksize):
	base = encryption_oracle(b"A")
	cipher = encryption_oracle(b"A"*blocksize*3)
	blockIdx = getFirstDifferentBlockId(base, cipher, blocksize)
	return getBlockById(cipher, blockIdx+1, blocksize) == getBlockById(cipher, blockIdx+2, blocksize)
	
def detectCharacter(secretBeginning, prefixLength, blocksize):
	secretBeginningLen = prefixLength + len(secretBeginning)
	prefix = b"A" * (blocksize - (secretBeginningLen % blocksize) - 1)
	blockId = secretBeginningLen // blocksize
	correctCipherBlock = getBlockById(encryption_oracle(prefix), blockId, blocksize)
	for idx in range(256):
		candidateCipher = encryption_oracle(prefix + secretBeginning + bytes([idx]))
		if getBlockById(candidateCipher, blockId, blocksize) == correctCipherBlock:
			return bytes([idx])

			
blocksize = getBlockSize()
prefixLength, suffixLength = getCipherInfos(blocksize)
print("block size is {}".format(blocksize))
print("prefix size is {}".format(prefixLength))
print("suffix size is {}".format(suffixLength))

if isAES_ECB(blocksize):
	print("AES ECB is used")
	secret = b""
	idx = 0
	while idx < suffixLength:
		secretChar = detectCharacter(secret, prefixLength, blocksize)
		secret += secretChar
		idx += 1
	print("Secret found : {}".format(secret))