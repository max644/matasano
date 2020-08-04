import MT19937RNG
import random

candidateRng = MT19937RNG.MT19937RNG()
candidateRng.seed_mt(random.randint(0, 0xFFFFFFFFFFFFFFFF))

constants = MT19937RNG.MT19937RNG()
# y = y ^ (y >> self.l)
def reverseTemp1(nb):
    hi = (nb ^ 0) & 0xffffc000
    lo = ((nb & 0x3FFF) ^ (hi >> constants.l))
    return hi | lo
    
# y = y ^ ((y << self.t) & self.c)
def reverseTemp2(nb):
    lo = (nb ^ (0 & constants.c)) & 0x1ffff
    hi = nb ^ ((lo << constants.t) & constants.c)
    return hi | lo

# y = y ^ ((y << self.s) & self.b)    
def reverseTemp3(nb):
    lo = (nb ^ (0 & constants.b)) & 0x7f # [-7:]
    mid1 = (nb ^ ((lo << constants.s) & constants.b)) & 0x3f80# [-14:-7]
    mid2 = (nb ^ ((mid1 << constants.s) & constants.b)) & 0x1fc000# [-21:-14]
    mid3 = (nb ^ ((mid2 << constants.s) & constants.b)) & 0xfe00000# [-28:-21]
    mid4 = (nb ^ ((mid3 << constants.s) & constants.b)) & 0xf0000000# [-32:-28]
    return lo | mid1 | mid2 | mid3 | mid4
    
# y = y ^ (y >> self.u)
def reverseTemp4(nb):
    hi = (nb ^ 0) & 0xffe00000 # 11 first
    mid1 = ((nb & 0x1ffc00) ^ (hi >> constants.u)) # 11 next
    mid2 = ((nb & 0x3ff) ^ (mid1 >> constants.u)) # 11 next
    return hi | mid1 | mid2
    
def reverseTempering(nb):
    return reverseTemp4(reverseTemp3(reverseTemp2(reverseTemp1(nb))))
    
randNumbers = [candidateRng.extract_number() for _ in range(624)]
MT = [reverseTempering(randNumber) for randNumber in randNumbers]

# test with next 10 randoms : 
rngClone = MT19937RNG.MT19937RNG()
rngClone.MT = MT # initialise with recovered randoms
rngClone.index = 624 # set the index to correct position (next call to extract_number will trigger twist)
for idx in range(10):
    print("2 randoms equals" if candidateRng.extract_number() == rngClone.extract_number() else "randoms are not equals")