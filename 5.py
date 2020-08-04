import utils

if __name__ == "__main__":
	plain = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
	key = b"ICE"
	cipher = utils.xor(plain, key)
	print("({}, {}) => {}".format(plain, key, utils.strToHex(cipher)))