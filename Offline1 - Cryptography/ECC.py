import PRIME

import secrets
import time


# https://neuromancer.sk/std/x962/prime256v1
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
G = {"x": 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
      "y":0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5}
keyLength = [128, 192, 256]


def extendGCD(a1, a2):
    # gcd, x, y
    if a1 == 0: return a2, 0, 1
    else:
        tempMod = a2 % a1
        gcd, x, y = extendGCD(tempMod, a1)
        y = y - (a2 // a1) * x
        return gcd, y, x


def invMOD(a1, prime):
    g, x, y = extendGCD(a1, prime)
    return None if g != 1 else x % prime


def add(Point1, Point2, prime):
    P2x = Point2["x"]
    P1x = Point1["x"]
    P2y = Point2["y"]
    P1y = Point1["y"]

    slope = 0

    if P2x- P1x > 0:
        numerator = (P2y - P1y) % prime
        denominator = invMOD(P2x - P1x, prime)
        slope = (numerator * denominator) % prime
    else:
        numerator = (-P2y + P1y) % prime
        denominator = invMOD(-P2x + P1x, prime)

        slope = (numerator * denominator) % prime

    xAdd = (slope ** 2 - P1x - P2x) % prime
    yAdd = (slope * (P1x - xAdd) - P1y) % prime
    
    temp = {}
    temp["x"] = xAdd
    temp["y"] = yAdd

    return temp



# y^2 = x^3 + ax + c
# 2y*dy/dx = 3x^2 + a
def double(Point, a, prime):
    Px = Point["x"]
    Py = Point["y"]
    
    numerator = (3 * Px ** 2 + a) % prime
    denominator = invMOD(2 * Py, prime)
    
    slope = (numerator * denominator) % prime

    xDouble = (slope ** 2 - 2 * Px) % prime
    yDouble = (slope * (Px - xDouble) - Py) % prime

    temp = {}
    temp["x"] = xDouble
    temp["y"] = yDouble
    
    return temp



def doubleAdd(mScaler, Point, a, prime):
    bits = bin(mScaler)[2:]
    temp = Point
    n = len(bits)
    
    for i in range(1, n):
        # 0 -> double
        # 1 -> double + 1
        temp = double(temp, a, prime)
      
        if (bits[i] == "1"):
            temp = add(Point, temp, prime)
    
    return temp

def ECDH_AESkey(otherPublicKey, myPrivateKey, a, prime):
    commonKey = doubleAdd(myPrivateKey, otherPublicKey, a, prime)["x"]
    return commonKey

def ECDHpublicKey(myPrivateKey, Point, a, prime):
    publicKey = doubleAdd(myPrivateKey, Point, a, prime)
    return publicKey




def main():
    AT, BT, RT, paramGenT = [0]*3, [0]*3, [0]*3, [0]*3
    n =  len(keyLength)

    for i in range(n):
        
        sT = time.time()
        prime = PRIME.primeGen(keyLength[i])
        print(prime)
        eT = time.time()

        paramGenT[i] = eT - sT

        # alice public Ka generation
        sTalice = time.time()
        
        temp = secrets.token_bytes(keyLength[i])
        temp = int.from_bytes(temp, 'big')

        Ka = temp % prime
        publicAlice = ECDHpublicKey(Ka, G, a, prime)
        
        eTalice = time.time()

        AT[i] = eTalice - sTalice


        # bobs public Kb generation
        sTbob = time.time()
        
        temp = secrets.token_bytes(keyLength[i])
        temp = int.from_bytes(temp, 'big')

        Kb = temp % prime
        publicBob = ECDHpublicKey(Kb, G, a, prime)
        eTbob = time.time()

        BT[i] = eTbob - sTbob


        # common key generation in each side
        sTcommon = time.time()
        
        Ra = ECDH_AESkey(publicBob, Ka, a, prime)
        Rb = ECDH_AESkey(publicAlice, Kb, a, prime)
        
        eTcommon = time.time()

        RT[i] = eTcommon - sTcommon

        print(Ra, Rb)


    print("Computation Time:")
    

    def printData(keyLength, paramGenT, AT, BT, RT):
        n = len(keyLength)
        
        for i in range(n):    
            print(keyLength[i], end = " ")
            print(":")

            print("param generation time: ", end=" ")
            print(paramGenT[i] * 100, end=" ")
            print(" ms")

            print("A: ", end=" ")
            print(AT[i] * 100, end=" ")
            print(" ms")

            print("B: ", end=" ")
            print(BT[i] * 100, end=" ")
            print(" ms")


            print("Shared Key: ", end=" ")
            print(RT[i] * 100, end=" ")
            print(" ms")


    printData(keyLength, paramGenT, AT, BT, RT)


if __name__ == "__main__":
    main()