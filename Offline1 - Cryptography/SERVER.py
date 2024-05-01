import ECC
import AES

import socket
import secrets


keyLength = [128, 192, 256]


def server():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server = ('localhost', 12345)
    serverSocket.bind(server)

    print("Hello from Server!")
    serverSocket.listen(1)


    clientSocket, client = serverSocket.accept()

    try:
        paramFromClient = clientSocket.recv(1024).decode('utf-8').split('\n')

        p, a = int(paramFromClient[0]), int(paramFromClient[1])
        G = {}
        G["x"] = int(paramFromClient[3])
        G["y"] = int(paramFromClient[4])
      

        tempA = clientSocket.recv(1024).decode('utf-8').split('\n')
        
        A = {}
        A["x"] = int(tempA[0])
        A["y"] = int(tempA[1])
   
        
        temp = secrets.token_bytes(128)
        Kb = int.from_bytes(temp, 'big')
        B = ECC.ECDHpublicKey(Kb, G, a, p)
       
        x = B["x"]
        y = B["y"]
        tempB = f"{x}\n{y}"

        clientSocket.sendall(tempB.encode('utf-8'))

        sharedKey = ECC.ECDH_AESkey(A, Kb, a, p)
   
        sharedKeyBytes = sharedKey.to_bytes(16, byteorder= 'big')

        key = ""
        for x in range(len(sharedKeyBytes)):
            key += chr(sharedKeyBytes[x])

        cipher = clientSocket.recv(1024).decode('utf-8')
        decipher = AES.decrypt(key, cipher)
        
        print("reveived encrypted message: ", cipher)
        print("decrypted message: ", decipher)

        

    finally:
        clientSocket.close()

if __name__ == "__main__":
    server()
