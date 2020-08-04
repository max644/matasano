import utils
from random import randint
from copy import deepcopy

SECRETS = (
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
)

#SECRETS = ("TGUgTG9yZW0gSXBzdW0gZXN0IHNpbXBsZW1lbnQgZHUgZmF1eCB0ZXh0ZSBlbXBsb3mCIGRhbnMgbGEgY29tcG9zaXRpb24gZXQgbGEgbWlzZSBlbiBwYWdlIGF2YW50IGltcHJlc3Npb24uIExlIExvcmVtIElwc3VtIGVzdCBsZSBmYXV4IHRleHRlIHN0YW5kYXJkIGRlIGwnaW1wcmltZXJpZSBkZXB1aXMgbGVzIGFuboJlcyAxNTAwLCBxdWFuZCB1biBwZWludHJlIGFub255bWUgYXNzZW1ibGEgZW5zZW1ibGUgZGVzIG1vcmNlYXV4IGRlIHRleHRlIHBvdXIgcoJhbGlzZXIgdW4gbGl2cmUgc3CCY2ltZW4gZGUgcG9saWNlcyBkZSB0ZXh0ZS4gSWwgbidhIHBhcyBmYWl0IHF1ZSBzdXJ2aXZyZSBjaW5xIHNpimNsZXMsIG1haXMgcydlc3QgYXVzc2kgYWRhcHSCIIUgbGEgYnVyZWF1dGlxdWUgaW5mb3JtYXRpcXVlLCBzYW5zIHF1ZSBzb24gY29udGVudSBuJ2VuIHNvaXQgbW9kaWZpgi4gSWwgYSCCdIIgcG9wdWxhcmlzgiBkYW5zIGxlcyBhbm6CZXMgMTk2MCBncoNjZSCFIGxhIHZlbnRlIGRlIGZldWlsbGVzIExldHJhc2V0IGNvbnRlbmFudCBkZXMgcGFzc2FnZXMgZHUgTG9yZW0gSXBzdW0sIGV0LCBwbHVzIHKCY2VtbWVudCwgcGFyIHNvbiBpbmNsdXNpb24gZGFucyBkZXMgYXBwbGljYXRpb25zIGRlIG1pc2UgZW4gcGFnZSBkZSB0ZXh0ZSwgY29tbWUgQWxkdXMgUGFnZU1ha2VyLg==",)
BLOCKSIZE = 32 if randint(1, 2) == 1 else 16
KEY = utils.randomString(BLOCKSIZE)
IV = utils.randomString(BLOCKSIZE)

def getRandomSecret():
    return utils.b64Decode(SECRETS[randint(0, len(SECRETS) - 1)])
    
def encrypt():
    return utils.AES_CBC_encrypt(KEY, IV, getRandomSecret()), IV
    
def decrypt(cipher):
    try:
        utils.AES_CBC_decrypt(KEY, IV, cipher)
        return True
    except Exception as ex:
        return False

def changeStrChar(string, idx, character):
    return string[:idx] + character + string[idx+1:]
    
def recursiveCBCPadding(end, validCipher, iv, blocksize):
    # if we've found all secret bytes
    if len(end) == len(validCipher) - blocksize:
        return utils.pkcs7_unpad(bytes(reversed(end)))
        
    # save valid cipher before modify it
    cipher = deepcopy(validCipher)
    
    # nb of byes to remove from cipher (== number of blocks found * blocksize)
    bytesToRemove = (len(end) // blocksize) * blocksize
    if bytesToRemove > 0:
        cipher = cipher[:-bytesToRemove]
        
    # bytes sequence fox xoring
    xorBytes = cipher[:-blocksize]
    # padding target
    paddingByteValue = (len(end) % blocksize) + 1
    
    # setup block n - 1 to have correct padding
    for idx, byte in enumerate(end[-paddingByteValue+1:]):
        NthByte = (idx % blocksize) + 1
        byteToReplaceIdx = len(cipher) - blocksize - NthByte
        byteToXorIdx = -NthByte
        cipher = changeStrChar(cipher, byteToReplaceIdx, bytes([byte ^ xorBytes[byteToXorIdx] ^ paddingByteValue]))
    
    # guess a byte and recurse
    byteToReplaceIdx = len(cipher) - blocksize - paddingByteValue
    for candidate in range(256):
        cipher = changeStrChar(cipher, byteToReplaceIdx, bytes([candidate ^ xorBytes[-paddingByteValue] ^ paddingByteValue]))
        if decrypt(cipher):
            end2 = deepcopy(end)
            end2.append(candidate)
            secret = recursiveCBCPadding(end2, validCipher, iv, blocksize)
            if secret != None:
                return secret
    
    # no byte found
    return None

if __name__ == "__main__":
    cipher, iv = encrypt()
    print(recursiveCBCPadding([], iv + cipher, iv, BLOCKSIZE))