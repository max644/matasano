import utils
from sha1 import SHA1
import random
import binascii
import struct


# server
KEY = utils.randomString(random.randint(10, 10))

def secureMessageWithMAC(message):
    sha1 = SHA1()
    hash = binascii.hexlify(sha1.hash(KEY + message))
    return (message, hash)

def isMessageValidMAC(message, signature):
    sha1 = SHA1()
    print(sha1.hash(KEY + b"A"*100))
    hash = binascii.hexlify(sha1.hash(KEY + message))
    print(hash)
    print(signature)
    return hash == signature

message, signature = secureMessageWithMAC(b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon")

# client
MESSAGE_EXTENTION = b";admin=true"

for keysize in range(10, 11):
    messageLength = len(message)+ keysize
    
    sha1 = SHA1()
    gluePadding = sha1.padMessage(b"A" * keysize + message, messageLength)[keysize + len(message):]
    newMessage = message + gluePadding + MESSAGE_EXTENTION
    
    newMessageLength = keysize + len(newMessage) 
    
    sha1 = SHA1()
    sha1.h0 = struct.unpack(">I", binascii.unhexlify(signature[0:8]))[0]
    sha1.h1 = struct.unpack(">I", binascii.unhexlify(signature[8:16]))[0]
    sha1.h2 = struct.unpack(">I", binascii.unhexlify(signature[16:24]))[0]
    sha1.h3 = struct.unpack(">I", binascii.unhexlify(signature[24:32]))[0]
    sha1.h4 = struct.unpack(">I", binascii.unhexlify(signature[32:40]))[0]
    
    newSignature = binascii.hexlify(sha1.hash(MESSAGE_EXTENTION, newMessageLength))
    
    print(keysize, isMessageValidMAC(newMessage, newSignature))
    
#                                                                                                                                                                                                                                                                             ;admin=true\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04X
#\xbf\x03\x8b\x83\x8dM\xf3gfScomment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xb8;admin=true\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04X
#