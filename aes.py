from BitVector import *
from numpy import size
import bitvectordemo
# bv = BitVector(hexstring="02")
# print(bv)


# plainText = "CanTheyDoTheirFest"
# plainTextHex = plainText.encode('utf-8').hex()

# key = "BUET   
# keyHex = key.encode('utf-8').hex()

def printhex(a):
    myhexstring = a.get_bitvector_in_hex()
    print(f'{a},{myhexstring}')

RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36]
w=[]

def ByteSub(vec):
    for i in range(0,32,8):
        vec[i:i+8]=BitVector(intVal=bitvectordemo.Sbox[vec[i:i+8].intValue()],size=8)
    return vec

def AddRoundKey(round,state):
    return state^w[round*4]


def KeyExpansion(key,keysize):
    key = getHexFromAscii(key)
    key = BitVector(hexstring = key)
    print(key)
    for i in range(0,keysize,32):
        w.append(key[i:i+32])
    
    
    for i in range(0,10):
        newWord=w[4*(i+1)-1][8:32]+w[4*(i+1)-1][0:8] #circular byte left-shift
        newWord = ByteSub(newWord) #byte substitution
        rc = BitVector(intVal=RCON[i], size=8)
        rc = rc + BitVector(intVal = 0, size = 24)
        newWord=rc^newWord ##adding round constant
        w.append(newWord^w[4*i])
        w.append(w[4*(i+1)]^w[4*i+1])
        w.append(w[4*(i+1)+1]^w[4*i+2])
        w.append(w[4*(i+1)+2]^w[4*i+3])

    # w=[]
    # key = getHexFromAscii(key)
    # key = BitVector(hexstring = key)
    # print(key)
    # for i in range(0,keysize,32):
    #     w.append(key[i:i+32])
    # w.append(w[3])

    # w[4]=w[4]<<8
    # print(w[4],"hmm")
    # myhexstring = w[4].get_bitvector_in_hex()
    # print(f'{w[4]},{myhexstring}',{bytearray.fromhex(myhexstring).decode()})

    # w[4] = ByteSub(w[4])
    # print(type(w[4]),"hmm2")
    # myhexstring = w[4].get_bitvector_in_hex()
    # print(f'{w[4]},{myhexstring}')
    # rc = BitVector(intVal=RCON[0], size=8)
    # rc = rc + BitVector(intVal = 0, size = 24)
    # print(f'rc={rc}')
    # printhex(rc)
    # w[4]=rc^w[4]
    # myhexstring = w[4].get_bitvector_in_hex()
    # print(f'{w[4]},{myhexstring}')
    # w[4]=w[4]^w[0]
    # myhexstring = w[4].get_bitvector_in_hex()
    # print(f'{w[4]},{myhexstring}')
    # return w

"""Get hex representation of an ascii string"""
def getHexFromAscii(str):
    return str.encode('utf-8').hex()

    
def main():

    # a=BitVector(hexstring="5")
    # b=BitVector(hexstring="0")
    # c=a+b
    # print(type(c))
    # printhex(c)

    plainText = "Two One Nine Two"
    plainTextHex = plainText.encode('utf-8').hex()
    print(plainTextHex)

    key = "Thats my Kung Fu"
    keyHex = key.encode('utf-8').hex()

    print(keyHex)

    print("============")

    KeyExpansion(key,128)
    for idx,el in enumerate(w):
        myhexstring = el.get_bitvector_in_hex()
        print(f'idx-{idx}->{el},{myhexstring}',{bytearray.fromhex(myhexstring).decode(errors="ignore")})
    
        




    print(type(bitvectordemo.Sbox[23]))

    print("1st state")
    print(AddRoundKey(0,BitVector(hexstring=plainText)))




if __name__=="__main__":
    main()