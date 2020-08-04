import utils

BLOCKSIZE = 16
KEY = utils.randomString(BLOCKSIZE)

SECRET_PLAIN_STR = utils.b64Decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")

def encryption_oracle(plain):
    return utils.AES_ECB_encrypt(KEY, plain + SECRET_PLAIN_STR)

    
def getBlockSizeAndSecretLength():
    initLen = len(encryption_oracle(b"A"))
    cipherSize = 1
    curCipherSize = initLen
    while curCipherSize == initLen:
        cipherSize += 1
        curCipherSize = len(encryption_oracle(b"A"*cipherSize))
    blockSize = curCipherSize-initLen
    secretLength = curCipherSize-cipherSize-(blockSize)
    return blockSize, secretLength

def isAES_ECB(blockSize):
    cipher = encryption_oracle(b"A"*blockSize*2)
    return cipher[0:blockSize] == cipher[blockSize:blockSize*2]
    
def detectCharacter(secretBeginning):
    secretBeginningLen = len(secretBeginning)
    prefix = b"A" * (blockSize - (secretBeginningLen % blockSize) - 1)
    blockId = secretBeginningLen // blockSize
    correctCipherBlock = encryption_oracle(prefix)[blockSize*blockId:blockSize*(blockId+1)]
    for idx in range(256):
        candidateCipher = encryption_oracle(prefix + secretBeginning + bytes([idx]))
        if candidateCipher[blockSize*blockId:blockSize*(blockId+1)] == correctCipherBlock:
            return bytes([idx])

blockSize, secretLength = getBlockSizeAndSecretLength()
print("block size is {}".format(blockSize))
print("secret size is {}".format(secretLength))
if isAES_ECB(blockSize):
    print("AES ECB is used")
    secret = b""
    idx = 0
    while idx < secretLength:
        secretByte = detectCharacter(secret)
        secret += secretByte
        idx += 1
    print("Secret found : {}".format(secret))