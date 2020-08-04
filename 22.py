import MT19937RNG as random
import time

currentTs = int(time.time())

rng = random.MT19937RNG()
rng.seed_mt(currentTs)

targetRandomNumber = rng.extract_number()

idx=1579200000
found = False
candidateRng = random.MT19937RNG()
while not found:
	idx += 1
	candidateRng.seed_mt(idx)
	if candidateRng.extract_number() == targetRandomNumber:
		found = True

	if idx % 1000 == 0:
		print(idx)

print("==> {}".format(idx))

