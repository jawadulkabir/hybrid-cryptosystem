from tempfile import tempdir
from BitVector import *
import numpy as np
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
mixColMatrix = np.array([[2,3,1,1],
                         [1,2,3,1],
                         [1,1,2,3],
                         [3,1,1,2]])

"""byte substitution useing sBox"""
def ByteSub(vec,size):
    for i in range(0,size,8):
        vec[i:i+8]=BitVector(intVal=bitvectordemo.Sbox[vec[i:i+8].intValue()],size=8)
    return vec

"""takes input the round and a 128 bit BitVector as state matrix"""
def AddRoundKey(round,state):
    print("inside roundkey funx")
    roundKey = w[round*4]+w[round*4+1]+w[round*4+2]+w[round*4+3]
    # printhex(roundKey)
    # printhex(state) 
    return state^roundKey


def KeyExpansion(key,keysize):
    key = getHexFromAscii(key)
    key = BitVector(hexstring = key)
    print(key)
    for i in range(0,keysize,32):
        w.append(key[i:i+32])
    
    for i in range(0,10):
        newWord=w[4*(i+1)-1][8:32]+w[4*(i+1)-1][0:8] #circular byte left-shift
        newWord = ByteSub(newWord,32) #byte substitution
        rc = BitVector(intVal=RCON[i], size=8)
        rc = rc + BitVector(intVal = 0, size = 24)
        newWord=rc^newWord ##adding round constant
        w.append(newWord^w[4*i])
        w.append(w[4*(i+1)]^w[4*i+1])
        w.append(w[4*(i+1)+1]^w[4*i+2])
        w.append(w[4*(i+1)+2]^w[4*i+3])

"""shift rows of the input BitVector accordingly"""
def ShiftRow(state):
    #construct temporary nparray from bitvector
    temp = np.zeros(shape=(4,4),dtype=int)
    for j in range(4):  
        for i in range(4):
            loc=j*4+i
            temp[i,j]=state[loc*8:loc*8+8].intValue()
    
    #left shift each row of array accordingly
    for i in range(1,4):
        temp[i,:]=np.roll(temp[i,:],-i)

    #bitvector from nparray
    ret = BitVector(size = 0)
    for j in range(4):
        for i in range(4):
            loc=j*4+i
            ret += BitVector(intVal=temp[i,j],size=8)
    return ret    


def MixColumn(state):
    #construct temporary nparray from bitvector
    temp = np.zeros(shape=(4,4),dtype=int)
    ans = np.zeros(shape=(4,4),dtype=int)
    for j in range(4):  
        for i in range(4):
            loc=j*4+i
            temp[i,j]=state[loc*8:loc*8+8].intValue()
    
    #finite field multiplication
    AES_modulus = BitVector(bitstring='100011011')

    for i in range(4):
        for j in range(4):
            for k in range(4):
                a = BitVector(intVal=mixColMatrix[i,k],size=8)
                b = BitVector(intVal=temp[k,j],size=8)
                # print(f'{a},{b},{a.gf_multiply(b)}')
                # print(a.gf_multiply(b).intValue())
                # print("before:",ans[i,j])
                ans[i,j]^=a.gf_multiply_modular(b,AES_modulus,8).intValue()
                # print("aftere:",ans[i,j])
    print(ans)
    #bitvector from nparray
    ret = BitVector(size = 0)
    for j in range(4):
        for i in range(4):
            loc=j*4+i
            ret += BitVector(intVal=ans[i,j],size=8)
            # printhex(ret)
    return ret 




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
        #print(f'idx-{idx}->{el},{myhexstring}',{bytearray.fromhex(myhexstring).decode(errors="ignore")})
    
           
    print("1st state")
    state = AddRoundKey(0,BitVector(hexstring=plainTextHex))
    printhex(state)


    print("\nsubbyte")
    state = ByteSub(state,128)
    printhex(state)

    state = ShiftRow(state)
    print("after shift row:")
    printhex(state)

    state = MixColumn(state)
    print("after mix col:")
    printhex(state)

    state = AddRoundKey(1,state)
    print("after round 1:")
    printhex(state)




if __name__=="__main__":
    main()