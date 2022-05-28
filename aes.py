from BitVector import *
import numpy as np
import codecs
import time


RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36]
Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]


"""byte substitution useing sBox"""
def ByteSub(vec,size):
    for i in range(0,size,8):
        vec[i:i+8]=BitVector(intVal=Sbox[vec[i:i+8].intValue()],size=8)
    return vec

def InvByteSub(vec,size):
    for i in range(0,size,8):
        vec[i:i+8]=BitVector(intVal=InvSbox[vec[i:i+8].intValue()],size=8)
    return vec



"""takes input the round and a 128 bit BitVector as state matrix"""
def AddRoundKey(round,state,w):
    roundKey = w[round*4]+w[round*4+1]+w[round*4+2]+w[round*4+3]
    return state^roundKey


def KeyExpansion(key,keysize):
    w=[]
    key = getHexFromAscii(key)
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

def InvShiftRow(state):
    #construct temporary nparray from bitvector
    temp = np.zeros(shape=(4,4),dtype=int)
    for j in range(4):  
        for i in range(4):
            loc=j*4+i
            temp[i,j]=state[loc*8:loc*8+8].intValue()
    
    #left shift each row of array accordingly
    for i in range(1,4):
        temp[i,:]=np.roll(temp[i,:],i)

    #bitvector from nparray
    ret = BitVector(size = 0)
    for j in range(4):
        for i in range(4):
            loc=j*4+i
            ret += BitVector(intVal=temp[i,j],size=8)
    return ret   

"""mix columns of the state matrix using Galois field multiplication"""
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
                a = Mixer[i][k]
                b = BitVector(intVal=temp[k,j],size=8)
                ans[i,j]^=a.gf_multiply_modular(b,AES_modulus,8).intValue()
    
    ret = BitVector(size = 0)
    for j in range(4):
        for i in range(4):
            loc=j*4+i
            ret += BitVector(intVal=ans[i,j],size=8)
    return ret 


def InvMixColumn(state):
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
                a = InvMixer[i][k]
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

"""Get hex representation of an cipher string"""
def getHexFromCipher(str):
    return str.encode('cp437').hex()

def getCipherFromHex(hexStr):
    byteStr = bytes(hexStr, encoding='utf-8')
    binStr = codecs.decode(byteStr, "hex")
    return str(binStr, 'cp437')
#Cp1252


"""encrypt the plain text using extended key w"""
def encryption(w,plainText):
    plainTextHex = getHexFromAscii(plainText)
    
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


"""decrypt the cipher text using extended key w"""
def decryption(w,cipherText):
    cipherTextHex = getHexFromCipher(cipherText)

    state = AddRoundKey(10,BitVector(hexstring=cipherTextHex),w)

    for i in range(0,10):
        state = InvShiftRow(state)
        state = InvByteSub(state,128)
        state = AddRoundKey(9-i,state,w)
        if i!=9:
            state = InvMixColumn(state)

    plainText = state.get_bitvector_in_hex()
    return plainText


def validateInput(key,plainText):
    if(len(key)<16):
        extra = 16-len(key)
        key += chr(0)*extra  #add ascii value 0(null char) at the end
    elif(len(key)>16):
        key = key[0:16]
    
    pLen = len(plainText)
    if(pLen%16!=0):
        extra = 16-pLen%16
        plainText += chr(0)*extra
    return key, plainText


def main():
    plainText = "Two One Nine Two"

    key = "Thurigherer df"

    # plainText = "CanTheyDoTheirFe"

    # key = "BUET CSE17 Batch" 

    key, plainText = validateInput(key, plainText)
    print(key,len(key))
    print(plainText,len(plainText))

    keyStart = time.time()
    w=KeyExpansion(key,128)
    keyEnd = time.time()
    keyTime = keyEnd - keyStart


    print("Plain text:")
    print(plainText, "[In ASCII]")
    print(getHexFromAscii(plainText), "[In HEX]\n")

    print("Key:")
    print(key, "[In ASCII]")
    print(getHexFromAscii(key), "[In HEX]\n")

    print("============\n")

    encryptionStart = time.time()
    cipherHex = encryption(w,plainText)
    encryptionEnd = time.time()
    encryptionTime = encryptionEnd - encryptionStart

    print("Cipher Text:")
    print(cipherHex, "[In HEX]")
    print(getCipherFromHex(cipherHex), "[In ASCII]\n")

    


    decryptionStart = time.time()
    decipheredHex = decryption(w,getCipherFromHex(cipherHex))
    decryptionEnd = time.time()
    decryptionTime = decryptionEnd - decryptionStart

    print("Deciphered Text:")
    print(decipheredHex, "[In HEX]")
    print(getCipherFromHex(decipheredHex), "[In ASCII]\n")

    print("Execution Time")
    print(f'Key Scheduling: {keyTime} seconds')
    print(f'Encryption Time: {encryptionTime} seconds')
    print(f'Decryption Time: {decryptionTime} seconds')


if __name__=="__main__":
    main()