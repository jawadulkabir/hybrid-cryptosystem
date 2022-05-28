import socket,aes,rsa,pickle

s = socket.socket()		
print ("Socket successfully created")

port = 46975		
s.bind(('', port))		
print ("socket binded to %s" %(port))

s.listen(5)	
print ("socket is listening")		

plainText=""
def getData():
    global plainText
    plainText = input("Plain Text = ")
    aes_key = input("AES public key = ")
    K = input("Key length = ")

    aes_key, plainText = aes.validateInput(aes_key, plainText)

    w = aes.KeyExpansion(aes_key,128)
    cipherHex = aes.encryption(w,plainText)
    cipherText = aes.getCipherFromHex(cipherHex)
    rsa_keys = rsa.generateKey(K)
    rsa_public_key = [rsa_keys[0],rsa_keys[2]]
    rsa_private_key = [rsa_keys[1],rsa_keys[2]]
    encryptedKey = rsa.encryptMessage(aes_key,rsa_public_key[0],rsa_public_key[1])
    data = {
        'cipherText' : cipherText,
        'encryptedKey' : encryptedKey,
        'publicKey' : rsa_public_key
    }
    return rsa_private_key, data



private_key, data =getData()

f= open("dont open this.txt","w")
f.write(str(private_key[0]))
f.write("\n")
f.write(str(private_key[1]))
f.close()

while True:

    c, addr = s.accept()	
    print ('Got connection from', addr)


    data = pickle.dumps(data)
    c.send(data)

    ack = c.recv(1024)
    ack = pickle.loads(ack)  

    f = open("dont open this.txt", 'r')  # or os.remove(path)
    decipheredText = f.read()
    print("decrypted text = ",decipheredText)

    if plainText==decipheredText:
        print("MATCHES")
    else:
        print("DOES NOT MATCH")

    # print(f'{plainText}={decipheredText}')

    c.close()

    break


