import utils
import random

BLOCKSIZE = 16
KEY = utils.randomString(BLOCKSIZE)
NONCE = random.randint(0, 2 ** 64)

def isAdmin(plain):
    return b";admin=true;" in plain

def encrypt(plain):
    plain = plain.replace(b';', b'%3B').replace(b'=', b'%3D') + b";comment2=%20like%20a%20pound%20of%20bacon"
    return utils.AES_CTR_encrypt(KEY, NONCE, plain)
    
def decrypt(cipher):
    plain = utils.AES_CTR_decrypt(KEY, NONCE, cipher)
    print(plain)
    return isAdmin(plain)
    
def changeStrChar(string, idx, byte):
    return string[:idx] + byte + string[idx+1:]
    
cipher = encrypt(b"A"*BLOCKSIZE + b"AadminBtrue")
cipher = changeStrChar(cipher, BLOCKSIZE, bytes([ord("A") ^ cipher[BLOCKSIZE] ^ ord(";")]))
cipher = changeStrChar(cipher, BLOCKSIZE+6, bytes([ord("B") ^ cipher[BLOCKSIZE+6] ^ ord("=")]))
print(decrypt(cipher))