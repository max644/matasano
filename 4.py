import utils

if __name__ == "__main__":
	with open("4.txt", "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	
	maxScore = 0
	maxCipher = ""
	maxPlain = ""
	for line in lines:
		key, plain, score = utils.decypher1CharXor(utils.hexToStr(line))
		if score > maxScore:
			maxScore = score
			maxCipher = line
			maxPlain = plain
			
	print("Cipher {} : score is {} and plain is '{}'".format(maxCipher, maxScore, maxPlain))