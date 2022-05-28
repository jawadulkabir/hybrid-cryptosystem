from BitVector import *
import math

"""generate n prime numbers of k-bit length"""
def generatePrime(n,K):
    prime = 0
    primeList = []

    while prime<n:
        bv = BitVector(intVal = 0)
        bv = bv.gen_random_bits(K)  
        check = bv.test_for_primality()
        if check>0.9:
            prime += 1
            primeList.append(bv)
    return primeList

"""b^n modm"""
# def modularExp(b,n,m): 
#     n = bin(n)
#     n=n[2:]

#     x=1
#     power=b%m
#     for a in reversed(n):
#         if a=='1':
#             x = (x*power)%m
#         power = (power*power)%m
#     return x

def generateKey(K,ch):
    K = int(K/2)
    primeList=generatePrime(2,K)

    # p = primeList[0].intValue()
    # q = primeList[1].intValue()
    p=59617
    q=62633

    print(f'p={p}')
    print(f'q={q}')

    n = p*q
    # phi = (p-1)*(q-1)
    # e  = generatePrime(1,K-1)[0].intValue()
    # print(f'e={e}')
    # d = pow(e,-1,phi) #modulur multiplicative inverse #d*e = 1 (mod phi)
    # print(f'd={d}')

    e=25717
    d=3514776541

    cip = pow(ch,e,n)
    print(cip)
    print(pow(cip,d,n))

    #return e,d,n

def encryptNum(ch,e,n):
    return pow(ch,e,n)

def decryptNum(ch,d,n):
    return pow(ch,d,n)
    
def encryptMessage(msg,e,n):
    l = list(bytes(msg, 'ascii'))
    print("plaint-",l)
    cipher = []
    for item in l:
        C = encryptNum(item,e,n)
        cipher.append(C)
    return cipher
    
def decryptMessage(cipList,d,n):
    decipher = ""
    for item in cipList:
        d = decryptNum(item,d,n)
        print(d)
        #decipher += str(d)
    return decipher

def main():
    K = input()
    K = int(K)

    keys = generateKey(K,97)
    print(keys)
    # s = "balsal"
    # cip = encryptMessage(s,keys[0],keys[2])
    # print("cippher-",cip)

    # dec = decryptMessage(cip,keys[2],keys[2])
    # print(dec)


if __name__=="__main__":
    main()
    # x = 53
    # print(x)
    # print(chr(108))
    # print(str(x))


# C = pow(P,e,n)
#     print("cipher = ",C)
#     D = modularExp(C,d,n)
#     print("decipher = ",D)