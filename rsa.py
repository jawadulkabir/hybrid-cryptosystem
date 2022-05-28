from BitVector import *
import time

from tabulate import tabulate

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

def generateKey(K):
    K=int(K)
    K = int(K/2)
    primeList=generatePrime(2,K)

    p = primeList[0].intValue()
    q = primeList[1].intValue()

    n = p*q
    phi = (p-1)*(q-1)
    e  = generatePrime(1,K-1)[0].intValue()
    d = pow(e,-1,phi) #modulur multiplicative inverse #d*e = 1 (mod phi)

    return e,d,n

def encryptNum(ch,e,n):
    return pow(ch,e,n)

def decryptNum(ch,d,n):
    return pow(ch,d,n)
    
def encryptMessage(msg,e,n):
    msg = str(msg)
    l = list(bytes(msg, 'ascii')) #l now has all of msg characters in ascii value

    cipher = []
    for item in l:
        C = encryptNum(item,e,n)
        cipher.append(C)
    return cipher
    
def decryptMessage(cipList,d,n):
    decipher = ""
    for item in cipList:
        dec = decryptNum(item,d,n)
        decipher += chr(dec)
    return decipher

def main():
    keySizeList = [16,32,64,128]
    tableList=[]

    for K in keySizeList:
        tableItem = []
        tableItem.append(K)

        keyStart = time.time()
        keys = generateKey(K)   
        keyEnd = time.time()
        keyTime = keyEnd - keyStart
        tableItem.append(keyTime)

        print("Generated Keys")
        print(f"{{'public': ({keys[0]}, {keys[2]}), 'private': ({keys[1]}, {keys[2]})}}")
        

        s = "j0n bOn j8vi"
        print("Plain Text:")
        print(s)

        encryptionStart = time.time()
        cip = encryptMessage(s,keys[0],keys[2])
        encryptionEnd = time.time()
        encryptionTime = encryptionEnd - encryptionStart
        tableItem.append(encryptionTime)


        print("Cipher Text:")
        print(*cip, sep="\n")

        decryptionStart = time.time()
        dec = decryptMessage(cip,keys[1],keys[2])
        decryptionEnd = time.time()
        decryptionTime = decryptionEnd - decryptionStart
        tableItem.append(decryptionTime)

        print("Decrypted Text:")
        print(dec+"\n\n")

        tableList.append(tableItem)

    head = ["K","Key-Generation","Encryption","Decryption"]
    print(tabulate(tableList, headers=head, tablefmt="grid"))




if __name__=="__main__":
    main()