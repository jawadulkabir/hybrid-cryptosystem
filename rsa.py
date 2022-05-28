from BitVector import *
import math

# prime = 0
# primeList = []
# print(primeList)

# while prime<2:
#     bv = BitVector(intVal = 0)
#     bv = bv.gen_random_bits(32)  
#     check = bv.test_for_primality()
#     if check>0.9:
#         prime += 1
#         primeList.append(bv)

# print(primeList[0].get_bitvector_in_hex(),primeList[0].intValue())
# print(primeList[1].get_bitvector_in_hex(),primeList[1].intValue())

a=3945691776
b=3966371831

sa = int(math.sqrt(a))
sb = int(math.sqrt(b))

print(sa)
print(sb)

for i in range(2,sa+2):
    if a%i==0:
        print("got divisor of a")
        break


for i in range(2,sb+2):
    if b%i==0:
        print("got divisor of b")
        break