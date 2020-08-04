import utils

if __name__ == "__main__":
	print(utils.xor(utils.hexToStr("1c0111001f010100061a024b53535009181c"), utils.hexToStr("686974207468652062756c6c277320657965")) == utils.hexToStr("746865206b696420646f6e277420706c6179"))