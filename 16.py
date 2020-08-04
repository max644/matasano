import utils

BLOCKSIZE = 16
KEY = utils.randomString(BLOCKSIZE)
IV = utils.randomString(BLOCKSIZE)

def isAdmin(plain):
	return b";admin=true;" in plain

def encrypt(plain):
	plain = plain.replace(b';', b'%3B').replace(b'=', b'%3D') + b";comment2=%20like%20a%20pound%20of%20bacon"
	return utils.AES_CBC_encrypt(KEY, IV, plain)
	
def decrypt(cipher):
	plain = utils.AES_CBC_decrypt(KEY, IV, cipher)
	return isAdmin(plain)
	
def changeStrChar(string, idx, byte):
	return string[:idx] + byte + string[idx+1:]
	
cipher = encrypt(b"A"*BLOCKSIZE + b"AadminBtrue")
cipher = changeStrChar(cipher, 0, bytes([ord("A") ^ cipher[0] ^ ord(";")]))
cipher = changeStrChar(cipher, 6, bytes([ord("B") ^ cipher[6] ^ ord("=")]))
print(decrypt(cipher))