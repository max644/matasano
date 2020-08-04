import utils

print(utils.pkcs7_unpad(b"ICE ICE BABY\x04\x04\x04\x04") == b"ICE ICE BABY")

try:
	utils.pkcs7_unpad(b"ICE ICE BABY\x05\x05\x05\x05")
except Exception as ex:
	print("OK")
	
try:
	utils.pkcs7_unpad(b"ICE ICE BABY\x01\x02\x03\x04")
except Exception as ex:
	print("OK")