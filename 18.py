import utils

CIPHER = utils.b64Decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")
KEY = b"YELLOW SUBMARINE"
NONCE = 0

print(utils.ARS_CTR_encrypt(KEY, NONCE, CIPHER))