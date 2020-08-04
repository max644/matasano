from Crypto.Cipher import AES
from random import randint

HEX_DEC_MAP = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'A': 10,
    'B': 11,
    'C': 12,
    'D': 13,
    'E': 14,
    'F': 15,
    'a': 10,
    'b': 11,
    'c': 12,
    'd': 13,
    'e': 14,
    'f': 15,
}

DEC_HEX_MAP = {
    0: '0',
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: 'a',
    11: 'b',
    12: 'c',
    13: 'd',
    14: 'e',
    15: 'f',
}

DEC_B64_CHARSET = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'J',
    10: 'K',
    11: 'L',
    12: 'M',
    13: 'N',
    14: 'O',
    15: 'P',
    16: 'Q',
    17: 'R',
    18: 'S',
    19: 'T',
    20: 'U',
    21: 'V',
    22: 'W',
    23: 'X',
    24: 'Y',
    25: 'Z',
    26: 'a',
    27: 'b',
    28: 'c',
    29: 'd',
    30: 'e',
    31: 'f',
    32: 'g',
    33: 'h',
    34: 'i',
    35: 'j',
    36: 'k',
    37: 'l',
    38: 'm',
    39: 'n',
    40: 'o',
    41: 'p',
    42: 'q',
    43: 'r',
    44: 's',
    45:'t',
    46: 'u',
    47: 'v',
    48: 'w',
    49: 'x',
    50: 'y',
    51: 'z',
    52: '0',
    53: '1',
    54: '2',
    55: '3',
    56: '4',
    57: '5',
    58: '6',
    59: '7',
    60: '8',
    61: '9',
    62: '+',
    63: '/',
    64: '='
}

B64_DEC_CHARSET = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'I': 8,
    'J': 9,
    'K': 10,
    'L': 11,
    'M': 12,
    'N': 13,
    'O': 14,
    'P': 15,
    'Q': 16,
    'R': 17,
    'S': 18,
    'T': 19,
    'U': 20,
    'V': 21,
    'W': 22,
    'X': 23,
    'Y': 24,
    'Z': 25,
    'a': 26,
    'b': 27,
    'c': 28,
    'd': 29,
    'e': 30,
    'f': 31,
    'g': 32,
    'h': 33,
    'i': 34,
    'j': 35,
    'k': 36,
    'l': 37,
    'm': 38,
    'n': 39,
    'o': 40,
    'p': 41,
    'q': 42,
    'r': 43,
    's': 44,
    't': 45,
    'u': 46,
    'v': 47,
    'w': 48,
    'x': 49,
    'y': 50,
    'z': 51,
    '0': 52,
    '1': 53,
    '2': 54,
    '3': 55,
    '4': 56,
    '5': 57,
    '6': 58,
    '7': 59,
    '8': 60,
    '9': 61,
    '+': 62,
    '/': 63,
    '=': 0
}

ENGLISH_CHAR_FREQ = {
    ord('a'): 0.0651738,
    ord('b'): 0.0124248,
    ord('c'): 0.0217339,
    ord('d'): 0.0349835,
    ord('e'): 0.1041442,
    ord('f'): 0.0197881,
    ord('g'): 0.0158610,
    ord('h'): 0.0492888,
    ord('i'): 0.0558094,
    ord('j'): 0.0009033,
    ord('k'): 0.0050529,
    ord('l'): 0.0331490,
    ord('m'): 0.0202124,
    ord('n'): 0.0564513,
    ord('o'): 0.0596302,
    ord('p'): 0.0137645,
    ord('q'): 0.0008606,
    ord('r'): 0.0497563,
    ord('s'): 0.0515760,
    ord('t'): 0.0729357,
    ord('u'): 0.0225134,
    ord('v'): 0.0082903,
    ord('w'): 0.0171272,
    ord('x'): 0.0013692,
    ord('y'): 0.0145984,
    ord('z'): 0.0007836,
    ord('A'): 0.0651738,
    ord('B'): 0.0124248,
    ord('C'): 0.0217339,
    ord('D'): 0.0349835,
    ord('E'): 0.1041442,
    ord('F'): 0.0197881,
    ord('G'): 0.0158610,
    ord('H'): 0.0492888,
    ord('I'): 0.0558094,
    ord('J'): 0.0009033,
    ord('K'): 0.0050529,
    ord('L'): 0.0331490,
    ord('M'): 0.0202124,
    ord('N'): 0.0564513,
    ord('O'): 0.0596302,
    ord('P'): 0.0137645,
    ord('Q'): 0.0008606,
    ord('R'): 0.0497563,
    ord('S'): 0.0515760,
    ord('T'): 0.0729357,
    ord('U'): 0.0225134,
    ord('V'): 0.0082903,
    ord('W'): 0.0171272,
    ord('X'): 0.0013692,
    ord('Y'): 0.0145984,
    ord('Z'): 0.0007836,
    ord(' '): 0.1918182 
}

def hexToDec(hexDigits):
    return (HEX_DEC_MAP[hexDigits[0]] << 4) + HEX_DEC_MAP[hexDigits[1]]

def decToHex(decDigits, size = 0):
    output = hex(decDigits)[2:].replace("L", "")
    while len(output) < size:
        output = "0"+output
    return output

def strToHex(strInput):
    hexOutput = ""
    for carac in strInput:
        hexOutput += decToHex(carac, 2)
    return hexOutput

def hexToStr(hexInput):
    strOutput = []
    for idx in range(0, len(hexInput), 2):
        strOutput.append(hexToDec(hexInput[idx:idx+2]))
    return bytes(strOutput)
    
def b64Encode(strInput):
    output = ""
    for idx in range(0, len(strInput), 3):
        part = strInput[idx:idx+3]
        
        s1, s2, s3 = ord(part[0]), 0, 0
        if len(part) == 3:
            s2 = ord(part[1])
            s3 = ord(part[2])
        elif len(part) == 2:
            s2 = ord(part[1])
        elif len(part) == 1:
            s2 = 0
            s3 = 0
        
        b1 = DEC_B64_CHARSET[(s1 & 0xFC) >> 2]
        b2 = DEC_B64_CHARSET[((s1 & 0x03) << 4) + ((s2 & 0xF0) >> 4)]
        b3 = DEC_B64_CHARSET[((s2 & 0x0F) << 2) + ((s3 & 0xC0) >> 6)]
        b4 = DEC_B64_CHARSET[(s3 & 0x3F)]
        
        output += b1 + b2
        if len(part) >= 2:
            output += b3
        else:
            output += DEC_B64_CHARSET[64]
        if len(part) >= 3:
            output += b4
        else:
            output += DEC_B64_CHARSET[64]
    
    return output
    
def b64Decode(b64Input):
    output = []
    for idx in range(0, len(b64Input), 4):
        part = b64Input[idx:idx+4]
        
        b1, b2, b3, b4 = B64_DEC_CHARSET[part[0]], B64_DEC_CHARSET[part[1]], B64_DEC_CHARSET[part[2]], B64_DEC_CHARSET[part[3]]
        
        s1 = (b1 << 2) + ((b2 & 0x30) >> 4)
        s2 = ((b2 & 0x0F) << 4) + ((b3 & 0x3C) >> 2)
        s3 = ((b3 & 0x03) << 6) + b4

        output.append(s1)
        output.append(s2)
        output.append(s3)
    return bytes(output)

def xor(str, key):
    ret = []
    keyLength = len(key)
    for idx in range(len(str)):
        ret.append(str[idx] ^ key[idx % keyLength])
    return bytes(ret)



def computeScore(plain):
    return sum(ENGLISH_CHAR_FREQ[c] if c in ENGLISH_CHAR_FREQ else 0 for c in plain)
    
def decypher1CharXor(cipher):
    maxScore = 0
    validPlain = ""
    key = ""
    for x in range(256):
        plain = xor(cipher, bytes([x]))
        score = computeScore(plain)
        if score > maxScore:
            maxScore = score
            validPlain = plain
            key = bytes([x])
    return key, validPlain, maxScore
    
def AES_ECB_encrypt(key, raw, pad=True):
    aes = AES.new(key, AES.MODE_ECB)
    if pad:
        return aes.encrypt(pkcs7_pad(raw, len(key)))
    else:
        return aes.encrypt(raw)
        
def AES_ECB_decrypt(key, cipher, unpad=True):
    aes = AES.new(key, AES.MODE_ECB)
    if unpad:
        return pkcs7_unpad(aes.decrypt(cipher))
    else:
        return aes.decrypt(cipher)
    
def pkcs7_pad(plain, blocksize):
    paddingSize = blocksize-len(plain)%blocksize
    if paddingSize == 0:
        paddingSize = blocksize
    return plain + bytes([paddingSize]*paddingSize)
    
def pkcs7_unpad(plain):
    paddingSize = plain[-1]
    if plain[-paddingSize:] != bytes([paddingSize] * paddingSize):
        raise Exception('wrong padding') 
    return plain[0:len(plain)-paddingSize]

def AES_CBC_encrypt(key, iv, plain):
    cipher = b""
    previousBlock = iv
    blocksize = len(key)
    plain = pkcs7_pad(plain, blocksize)
    for idx in range(0, len(plain), blocksize):
        plainBlock = plain[idx:idx+blocksize]
        cipherBlock = AES_ECB_encrypt(key, xor(previousBlock, plainBlock), False)
        cipher += cipherBlock
        previousBlock = cipherBlock
    return cipher
    
def AES_CBC_decrypt(key, iv, cipher):
    plain = b""
    previousBlock = iv
    blocksize = len(key)
    for idx in range(0, len(cipher), blocksize):
        cipherBlock = cipher[idx:idx+blocksize]
        plain += xor(previousBlock, AES_ECB_decrypt(key, cipherBlock, False))
        previousBlock = cipherBlock
    return pkcs7_unpad(plain)
    
def randomString(size):
    return bytes([randint(0, 0xFF) for _ in range(size)])
    
def littleEndian(integer, size):
    output = b""
    for idx in range(size):
        output += bytes([((integer >> (idx * 8)) & 0xFF)])
    return output
    
def AES_CTR_encrypt(key, nonce, cipher, startBlockCount = 0):
    blocksize = len(key)
    blocksize2 = blocksize // 2
    leNonce = littleEndian(nonce, blocksize2)
    plain = b""
    for idx in range(len(cipher)):
        leBlockCount = littleEndian(idx + startBlockCount, blocksize2)
        plain += xor(cipher[idx*blocksize:(idx+1)*blocksize], AES_ECB_encrypt(key, leNonce + leBlockCount, False))
    return plain
    
def AES_CTR_decrypt(key, nonce, cipher, startBlockCount = 0):
    return AES_CTR_encrypt(key, nonce, cipher, startBlockCount)