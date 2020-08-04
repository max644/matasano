import utils
import random
import MT19937RNG
import struct

KEY = random.randint(0, 2 ** 16)
PREFIX = utils.randomString(random.randint(10, 100))

def encrypt(plain, key):
    prng = MT19937RNG.MT19937RNG()
    prng.seed_mt(KEY)
    keystream = b"".join(struct.pack('>I', prng.extract_number()) for _ in range(len(plain) // 4 + 1))
    cipher = utils.xor(plain, keystream)
    return cipher
    
def oracle(plain):
    return encrypt(PREFIX + plain, KEY)
    
print("ORIGINAL SEED : %d" % KEY)
    
cipher = oracle(b"A"*7) # 7 is enought to have an aligned block (% 4 == 0)

# compute last block aligned with a number from MT19937RNG ( % 4 == 0)
endBlock = len(cipher) - (len(cipher) % 4)
begBlock = endBlock - 4
idblock = begBlock // 4
block = cipher[begBlock:endBlock]

# recover the number used by oracle for my target block by xoring with my known plaintext ("AAAA")
keystreamBlock = utils.xor(block, b"AAAA")
number = struct.unpack(">I", keystreamBlock)[0]

# test all seeds and search the number of my target block
for candidateSeed in range(0, 2**16):
    candidatePrng = MT19937RNG.MT19937RNG()
    candidatePrng.seed_mt(candidateSeed)
    
    for _ in range(idblock):
        candidatePrng.extract_number()
        
    if candidatePrng.extract_number() == number:
        print("SEED FOUND : %d" % candidateSeed)