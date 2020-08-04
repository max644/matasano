import struct

class SHA1:
    def __init__(self):
        self.h0 = 0x67452301
        self.h1 = 0xEFCDAB89
        self.h2 = 0x98BADCFE
        self.h3 = 0x10325476
        self.h4 = 0xC3D2E1F0

    def leftRotate(self, nb, offset):
        return (nb << offset | nb >> 32 - offset)

    def padMessage(self, message, messageLength = -1):
        if messageLength == -1:
            ml = len(message) * 8
        else:
            ml = messageLength * 8

        message = message + b"\x80"
        message = message + b"\x00" * ((56 - len(message) % 64) % 64)
        message = message + struct.pack(">Q", ml)
        
        return message

    def hash(self, message, messageLength = -1):
    
        message = self.padMessage(message, messageLength)
        
        for chunkId in range(0, len(message), 64):
            chunk = message[chunkId: chunkId+64]
            words = [struct.unpack(">I", chunk[idx:idx+4])[0] for idx in range(chunkId, chunkId+64, 4)]
            
            for wordId in range(16, 80):
                words.append(self.leftRotate(words[wordId-3] ^ words[wordId-8] ^ words[wordId-14] ^ words[wordId-16], 1) & 0xffffffff)
            
            a, b, c, d, e = self.h0, self.h1, self.h2, self.h3, self.h4
            
            for idx in range(0, 80):
                if 0 <= idx and idx <= 19:
                    f = (b & c) | ((~b) & d)
                    k = 0x5A827999
                elif 20 <= idx and idx <= 39:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif 40 <= idx and idx <= 59:
                    f = (b & c) | (b & d) | (c & d) 
                    k = 0x8F1BBCDC
                elif 60 <= idx and idx <= 79:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6
                    
                temp = (self.leftRotate(a, 5) + f + e + k + words[idx]) & 0xFFFFFFFF
                e = d
                d = c
                c = (self.leftRotate(b, 30))
                b = a
                a = temp
            
            self.h0 = self.h0 + a & 0xFFFFFFFF
            self.h1 = self.h1 + b & 0xFFFFFFFF
            self.h2 = self.h2 + c & 0xFFFFFFFF
            self.h3 = self.h3 + d & 0xFFFFFFFF
            self.h4 = self.h4 + e & 0xFFFFFFFF

        hh = struct.pack(">I", self.h0) + struct.pack(">I", self.h1) + struct.pack(">I", self.h2) + struct.pack(">I", self.h3) + struct.pack(">I", self.h4)
        
        return hh