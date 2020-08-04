import utils

print(b"YELLOW SUBMARINE\x04\x04\x04\x04" == utils.pkcs7_pad(b"YELLOW SUBMARINE", 20))