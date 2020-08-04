from sha1 import SHA1
import binascii

sha1 = SHA1()
#print(binascii.hexlify(sha1.hash(b"test")))
print(binascii.hexlify(sha1.hash(b"A"*30))) # 2a22
# print(binascii.hexlify(sha1.hash(b"A"*31)))
# print(binascii.hexlify(sha1.hash(b"A"*32)))
# print(binascii.hexlify(sha1.hash(b"A"*33)))
# print(binascii.hexlify(sha1.hash(b"A"*34)))

# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA