import utils
from random import randint
from collections import defaultdict

BLOCKSIZE = 16
KEY = utils.randomString(BLOCKSIZE)
NONCE = randint(0, 0xFFFFFFFFFFFFFFFF)

if __name__ == "__main__":
    with open("19.txt", "r") as file:
        lines = file.readlines()
    
    plains = [utils.b64Decode(line[:-1]) for line in lines]

    ciphers = [utils.ARS_CTR_encrypt(KEY, NONCE, plain) for plain in plains]
    
    keystream = b""
    for idx in range(0, max([len(c) for c in ciphers])):
        candidateScore = defaultdict(int)
        for candidate in range(256):
            for c in ciphers:
                if len(c) > idx:
                    keystreamChar = c[idx] ^ candidate
                    if keystreamChar in utils.ENGLISH_CHAR_FREQ:
                        candidateScore[candidate] += utils.ENGLISH_CHAR_FREQ[keystreamChar]
        keystream += bytes([max(candidateScore, key=candidateScore.get)])
    
    for c in ciphers:
        print(utils.xor(c, keystream))