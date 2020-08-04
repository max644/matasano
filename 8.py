import utils

BLOCKSIZE = 16

def isAES_ECB(cipher):
	for i in range(0, len(cipher)-1, BLOCKSIZE):
		for j in range(i+BLOCKSIZE, len(cipher), BLOCKSIZE):
			if cipher[i:i+BLOCKSIZE] == cipher[j:j+BLOCKSIZE]:
				return True
	return False
	
with open("8.txt", "r") as file:
	lines = file.readlines()

lines = [line[:-1] for line in lines]

for idx, line in enumerate(lines):
	if isAES_ECB(utils.hexToStr(line)):
		print("Line number %d is AES ECB encrypted" % idx)