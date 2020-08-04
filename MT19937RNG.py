class MT19937RNG():
	def __init__(self):
		self.w, self.n, self.m, self.r = (32, 624, 397, 31)
		self.a = 0x9908B0DF
		(self.u, self.d) = (11, 0xFFFFFFFF)
		(self.s, self.b) = (7, 0x9D2C5680)
		(self.t, self.c) = (15, 0xEFC60000)
		self.l = 18
		self.f = 1812433253
		
		self.MT = list(range(0, self.n))
		self.index = self.n+1
		self.lower_mask = (1 << self.r) - 1
		self.upper_mask = 1 << self.r
		
	def seed_mt(self, seed):
		self.index = self.n
		self.MT[0] = seed
		for i in range(1, self.n):
			self.MT[i] = self.int_32(self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i)
			
	def extract_number(self):
		if self.index >= self.n:
			if self.index > self.n:
				raise Exception('Generator was never seeded', 'Generator was never seeded')
			self.twist()
		
		y = self.MT[self.index]
		#y = y ^ ((y >> self.u) & self.d)
		y = y ^ (y >> self.u)
		y = y ^ ((y << self.s) & self.b)
		y = y ^ ((y << self.t) & self.c)
		y = y ^ (y >> self.l)
		
		self.index = self.index + 1
		return self.int_32(y)
		
	def twist(self):
		for i in range(0, self.n):
			x = self.int_32((self.MT[i] & self.upper_mask) + (self.MT[(i+1) % self.n] & self.lower_mask))
			xA = x >> 1
			if (x % 2) != 0:
				xA = xA ^ self.a
			self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
		self.index = 0
		
	def int_32(self, number):
		return int(0xFFFFFFFF & number)