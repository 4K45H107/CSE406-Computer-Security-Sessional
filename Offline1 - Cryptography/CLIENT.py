import ECC
import AES
import PRIME

import socket
import secrets

a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
G = {"x": 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
      "y":0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5}



def client():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    server = ('localhost', 12345)
    clientSocket.connect(server)
    print("Thanks Server!!")

    try:

        prime = PRIME.primeGen(128)

        gx = G["x"]
        gy = G["y"]
        paramForServer = f"{prime}\n{a}\n{b}\n{gx}\n{gy}"
        
        clientSocket.sendall(paramForServer.encode('utf-8'))
       
        temp = secrets.token_bytes(128)
        Ka = int.from_bytes(temp, 'big')
        
        A = ECC.ECDHpublicKey(Ka, G, a, prime)
        
        x = A["x"]
        y = A["y"]
        
        tempA = f"{x}\n{y}"

        clientSocket.sendall(tempA.encode('utf-8'))

        tempB = clientSocket.recv(1024).decode('utf-8').split('\n')

        B = {}
        B["x"] = int(tempB[0])
        B["y"] = int(tempB[1])

        sharedKey = ECC.ECDH_AESkey(B, Ka, a, prime)
        sharedKeyBytes = sharedKey.to_bytes(16, byteorder="big")
        
        key = ""
        for x in range(len(sharedKeyBytes)):
            key += chr(sharedKeyBytes[x])

        message = input("Message: ")
        cipher, a1 ,a2  = AES.encrypt(key, message)
        print(cipher)

        print("Message: ", message)
        print("Encrypted message: ", cipher)

        clientSocket.sendall(cipher.encode('utf-8'))


    finally:
        clientSocket.close()

if __name__ == "__main__":
    client()
