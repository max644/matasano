import utils
import base64
import random

KEY = utils.randomString(16)
NONCE = random.randint(0, 2**128)

with open("25.txt", "r") as file:
    content = base64.b64decode("".join([line.strip() for line in file.readlines()]))

plain = utils.AES_ECB_decrypt(b"YELLOW SUBMARINE", content)
cipher = utils.AES_CTR_encrypt(KEY, NONCE, plain)

# ----------

def edit(cipher, offset, newplain):
    plain = utils.AES_CTR_decrypt(KEY, NONCE, cipher)
    plain = plain[:offset] + newplain + plain[offset+len(newplain):]
    return utils.AES_CTR_encrypt(KEY, NONCE, plain)

cipher2 = edit(cipher, 0, b"A" * len(cipher))
keystream = utils.xor(b"A" * len(cipher), cipher2)
plain = utils.xor(cipher, keystream)

print(plain)