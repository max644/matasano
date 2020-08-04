import utils

KEYSIZE_PROCEED_COUNT = 1

def hammingDistance(buf1, buf2):
	distance = 0
	for car1, car2 in zip(buf1, buf2):
		for idx in range(8):
			if ((car1 >> idx) & 0x01) != ((car2 >> idx) & 0x01):
				distance += 1
	return distance

def editDistance(cipher, keysize):
	word1 = cipher[0:keysize]
	totalDistance = 0
	distanceComputed = 0
	for idx in range(keysize, len(cipher), keysize):
		word2 = cipher[idx:idx+keysize]
		totalDistance += hammingDistance(word1, word2)
		distanceComputed += 1
	return float(totalDistance) / (distanceComputed*keysize)

def buildByteBlocks(cipher, keysize):
	blocks = []
	for idx in range(0, len(cipher), keysize):
		blocks.append(cipher[idx:idx+keysize])
		
	byteBlocks = []
	for byteIdx in range(0, keysize):
		byteBlock = []
		for block in blocks:
			if byteIdx < len(block):
				byteBlock.append(block[byteIdx])
		byteBlocks.append(byteBlock)
	return byteBlocks
	
if __name__ == "__main__":
	with open("6.txt", "r") as file:
		lines = file.readlines()
	
	content = ''.join(line[:-1] for line in lines)
	cipher = utils.b64Decode(content)
	
	keysizeAndDistance = []
	for keysize in range(2, 41):
		distance = editDistance(cipher, keysize)
		keysizeAndDistance.append((keysize, distance))
	
	keysizeAndDistance = sorted(keysizeAndDistance, key=lambda x:x[1])
	
	for idx in range(0, KEYSIZE_PROCEED_COUNT):
		keysize, distance = keysizeAndDistance[idx]
		byteBlocks = buildByteBlocks(cipher, keysize)
		
		key = b""
		for byteBlock in byteBlocks:
			key += utils.decypher1CharXor(byteBlock)[0]
	
		print("keysize : {} | key : {} | plain : {}".format(keysize, key, utils.xor(cipher, key)))