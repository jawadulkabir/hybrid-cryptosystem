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
def AddRoundKey(round,state,w):
    roundKey = w[round*4]+w[round*4+1]+w[round*4+2]+w[round*4+3]
    return state^roundKey


def KeyExpansion(key,keysize):
    w=[]
    key = getHexFromAscii(key)
    print(key)
    key = BitVector(hexstring = key)
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
    return w


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
                ans[i,j]^=a.gf_multiply_modular(b,AES_modulus,8).intValue()
    
    ret = BitVector(size = 0)
    for j in range(4):
        for i in range(4):
            loc=j*4+i
            ret += BitVector(intVal=ans[i,j],size=8)
    return ret 



"""Get hex representation of an ascii string"""
def getHexFromAscii(str):
    return str.encode('utf-8').hex()


def encryption(key,plainText):
    w=KeyExpansion(key,128)
    plainTextHex = getHexFromAscii(plainText)
    print(plainTextHex)
    
    #0th round
    state = AddRoundKey(0,BitVector(hexstring=plainTextHex),w)

    #10 rounds
    for i in range(1,11):
        state = ByteSub(state,128)
        state = ShiftRow(state)
        if i!=10:
            state = MixColumn(state)
        state = AddRoundKey(i,state,w)

    cipherText = state.get_bitvector_in_hex()
    return cipherText
    
    
def main():
    plainText = "Two One Nine Two"

    key = "Thats my Kung Fu"

    # plainText = "CanTheyDoTheirFe"

    # key = "BUET CSE17 Batch" 
    print("============")

    cipherText = encryption(key,plainText)
    print(cipherText)


if __name__=="__main__":
    main()