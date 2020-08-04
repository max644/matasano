import utils

B64_CHARSET = ('A', b'B', b'C', b'D', b'E', b'F', b'G', b'H', b'I', b'J', b'K', b'L', b'M', b'N', b'O', b'P', b'Q', b'R', b'S', b'T', b'U', b'V', b'W', b'X', b'Y', b'Z', b'a', b'b', b'c', b'd', b'e', b'f', b'g', b'h', b'i', b'j', b'k', b'l', b'm', b'n', b'o', b'p', b'q', b'r', b's', b't', b'u', b'v', b'w', b'x', b'y', b'z', b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'+', b'/', b'=')

def hexToB64(input):
	output = b""
	for idx in range(0, len(input), 6):
		part = input[idx:idx+6]
		suffix = 0
		
		h1, h2, h3 = utils.hexToDec(part[0:2]), 0, 0
		if len(part) == 6:
			h2 = utils.hexToDec(part[2:4])
			h3 = utils.hexToDec(part[4:6])
		elif len(part) == 4:
			h2 = utils.hexToDec(part[2:4])
		elif len(part) == 2:
			h2 = 0
			h3 = 0
		
		b1 = B64_CHARSET[(h1 & 0xFC) >> 2]
		b2 = B64_CHARSET[((h1 & 0x03) << 4) + ((h2 & 0xF0) >> 4)]
		b3 = B64_CHARSET[((h2 & 0x0F) << 2) + ((h3 & 0xC0) >> 6)]
		b4 = B64_CHARSET[(h3 & 0x3F)]
		
		output += b1 + b2
		if len(part) >= 4:
			output += b3
		else:
			output += B64_CHARSET[64]
		if len(part) >= 6:
			output += b4
		else:
			output += B64_CHARSET[64]
            
	return output
	
if __name__ == "__main__":
	print(hexToB64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d") == b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t")
	print(hexToB64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f") == b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb28=")
	print(hexToB64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f") == b"SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hybw==")