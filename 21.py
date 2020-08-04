import MT19937RNG as random


if __name__ == "__main__":
	rng = random.MT19937RNG()
	rng.seed_mt(5489)
	
	randomTargets = []
	with open("21.txt", "r") as file:
		randomTargets = file.readlines()
		
	randomTargets = [int(x[:-1]) for x in randomTargets]
	
	error = False
	for randomTarget in randomTargets:
		if randomTarget != rng.extract_number():
			error = True
			
	print("Error : " + str(error))
	
	