import utils

BLOCKSIZE = 16
KEY = IV = utils.randomString(BLOCKSIZE)

def isAdmin(plain):
    return b";admin=true;" in plain

def encrypt(plain):
    plain = plain.replace(b';', b'%3B').replace(b'=', b'%3D')
    return utils.AES_CBC_encrypt(KEY, IV, plain)
    
def decrypt(cipher):
    plain = utils.AES_CBC_decrypt(KEY, IV, cipher)
    for car in plain:
        if car >= 0x80:
            raise Exception(b'erreur de dechiffrage', plain)
    return plain
    
def changeStrChar(string, idx, byte):
    return string[:idx] + byte + string[idx+1:]
    
# sender
plain = b"A" * BLOCKSIZE * 3
cipher = encrypt(plain)

# attacker (man in the middle)
cipher = cipher[BLOCKSIZE*2:BLOCKSIZE*3] + b"\x00" * BLOCKSIZE + cipher[BLOCKSIZE*2:BLOCKSIZE*3] + cipher[BLOCKSIZE*3:]

# receiver
try:
    reply = decrypt(cipher)
except Exception as error:
    reply = error.args[0] + b" : " + error.args[1]
    
# attacker (man in the middle)
padding = len("erreur de dechiffrage : ")
iv = utils.xor(reply[padding:padding+BLOCKSIZE], reply[padding+BLOCKSIZE*2:padding+BLOCKSIZE*3])
print(iv == IV)
print(iv == KEY)
