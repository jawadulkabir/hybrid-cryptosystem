import socket,aes,rsa,pickle

s = socket.socket()        
 
port = 46975               
 
s.connect(('127.0.0.1', port))
data = s.recv(1024)
data = pickle.loads(data)   
print(data)

privateKey = None
while True:
    try:
        f = open("dont open this.txt", 'r')
        privateKey = f.read()
        privateKey = privateKey.split("\n")
        break
    except FileNotFoundError as e:
        pass


cipherText = data['cipherText']  
encryptedKey = data['encryptedKey']    

aes_key = rsa.decryptMessage(encryptedKey,int(privateKey[0]),int(privateKey[1]))
w = aes.KeyExpansion(aes_key,128)
decipheredHex = aes.decryption(w,cipherText)
decipheredText = aes.getCipherFromHex(decipheredHex)
print(decipheredText)


f= open("dont open this.txt","w")
f.write(str(decipheredText))
f.close()

ack = "ack"
ack = pickle.dumps(ack)
s.send(ack)
s.close()  



