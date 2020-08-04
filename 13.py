import utils

BLOCKSIZE = 16
KEY = utils.randomString(BLOCKSIZE)

def parseCookie(cookie):
	vars = cookie.split(b"&")
	obj = {}
	for var in vars:
		label, value = var.split(b"=")
		obj[label] = value
	return obj

def formatCookie(obj):
	return "&".join([key+"="+value for key, value in [("email", obj["email"]), ("uid", obj["uid"]), ("role", obj["role"])]])
		
	
def profile_for(emailAddr):
	return formatCookie({
		'email': emailAddr.replace("&", "").replace("=", ""),
		'uid': '10',
		'role': 'user'
	}).encode()

def encryption_oracle(emailAddr):
	return utils.AES_ECB_encrypt(KEY, profile_for(emailAddr))
	
def decrypt_oracle(cipher):
	plain = utils.AES_ECB_decrypt(KEY, cipher)
	print(plain)
	
def testIfAdmin(cipher):
	plain = utils.AES_ECB_decrypt(KEY, cipher)
	return parseCookie(plain)[b"role"] == b"admin"
	
# --------------------------------------------------------------------

# block0 : |email=AAAAAAAAAA|
# input : AAAAAAAAAA
# result : email=AAAAAAAAAA&uid=10&role=user
# blocks : AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCC
# block id to select : 0
block0 = encryption_oracle("AAAAAAAAAA")[0:BLOCKSIZE]

# block1 : |AAA&uid=10&role=|
# input : AAAAAAAAAAAAA
# result : email=AAAAAAAAAAAAA&uid=10&role=user
# blocks : AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCC
# block id to select : 1
block1 = encryption_oracle("AAAAAAAAAAAAA")[BLOCKSIZE:BLOCKSIZE*2]

# block2 : |admin&uid=10&rol|
# input : AAAAAAAAAAadmin
# result : email=AAAAAAAAAAadmin&uid=10&role=user
# blocks : AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCC
# block id to select : 1
block2 = encryption_oracle("AAAAAAAAAAadmin")[BLOCKSIZE:BLOCKSIZE*2]

# block3 : |=user|
# input : AAAAAAAAAAAAAA
# result : email=AAAAAAAAAAAAAA&uid=10&role=user
# blocks : AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCC
#block id to select : 2
block3 = encryption_oracle("AAAAAAAAAAAAAA")[BLOCKSIZE*2:BLOCKSIZE*3]

# block0 + block1 + block2 + block3
# email=AAAAAAAAAAAAA&uid=10&role=admin&uid=10&rol=user
print("admin ? : " + str(testIfAdmin(block0+block1+block2+block3)))