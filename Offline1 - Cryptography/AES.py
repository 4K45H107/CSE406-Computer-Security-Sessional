from BitVector import *
import time

def encrypt(KEY,PLAINTEXT):
    # import hoynai!!
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


    start = time.time()

    # adding round constant
    def roundKey(key,roundNum):

        roundMat = ["0x01","0x02","0x04","0x08","0x10","0x20","0x40","0x80","0x1b","0x36"]
        w = [[] for i in range(4)]

        # XOR
        def XOR(a1,a2):
            temp = []
            n = len(a1)
            for i in range(n):
                temp.append(hex(int(a1[i][2:],16) ^ int(a2[i][2:],16)))
            return temp


        # creating state matrix
        def stateMatrix(key):
            for i in range(4):
                for j in range(4):
                    w[i].append(key[4*i+j])
            return w
        
        # circular bit shift
        def circularBitShift(w):
            return list(w[3][1:] + w[3][:1])
        
        # byte substitution
        def byteSubstitution(gw):
            for i in range(4):
                b = BitVector(hexstring=gw[i][2:])
                int_val = b.intValue()
                s = Sbox[int_val]
                s = BitVector(intVal=s, size=8)
                gw[i] = s.get_bitvector_in_hex()
                # print(s.get_bitvector_in_hex())
            return gw
        
        # adding round constant
        def addRoundConstant(gw):
            gw[0] = hex(int(gw[0],16) ^ int(roundMat[roundNum][2:],16))[2:]
            for i in range(4):
                gw[i] = "0x" + gw[i]
            return gw
        
        #new key generation
        def newKeyGen(w,gw):
            tempW = [w[i] for i in range(4)]
            tempW.append(gw)


            for i in range(4):
                tempW.append(XOR(tempW[i],tempW[i+4]))
            
            tempKey = []
            for i in range(5,9):
                for j in range(4):
                    tempKey.append(tempW[i][j])
            return tempKey

        w = stateMatrix(key)
        gw = circularBitShift(w)    
        gw = byteSubstitution(gw)
        gw = addRoundConstant(gw) 
        nextKey = newKeyGen(w,gw)

        return nextKey

    def keyGeneration(KEY):
        # round 0 key
        key = []
        for c in KEY:
            key.append(hex(ord(c)))

        tempList = []
        tempList.append(key)
        for i in range(1,11):
            tempList.append(roundKey(tempList[i - 1],i - 1))
        return tempList

    # given
    nKey = len(KEY)

    print("Key: ")
    print("In ASCII: ", KEY)

    keyList = keyGeneration(KEY)
    
    endTime = time.time()
    keyGenTime = endTime - start
    
    start = time.time()

    key = keyList[0]

    print("In HEX: ", end="")
    for i  in range(len(key)):
        print(key[i][2:], end=" ")
    print()
    print()

    # ---------------------------------------------------------------------------------------


    # given
    n = len(PLAINTEXT)

    print("Plain Text: ")
    print("In ASCII: ", PLAINTEXT)
    # padding
    def padding(PLAINTEXT):
        extra = (nKey - n % nKey) % nKey
        for i in range(extra):
            PLAINTEXT += chr(0)
        return PLAINTEXT

    # plaintext in hex
    def plaintextHex(PLAINTEXT):
        plaintext = []
        for c in PLAINTEXT:
            plaintext.append(hex(ord(c)))
        return plaintext

    # plaintext into list of key size element
    def plaintTextToList(plaintext):
        plaintextList = []
        i = 0
        while i < n:
            temp = []
            for j in range(nKey):
                temp.append(plaintext[i+j])
            plaintextList.append(temp)
            i = i + nKey
        return plaintextList

    PLAINTEXT = padding(PLAINTEXT)
    plaintext = plaintextHex(PLAINTEXT)

    print("In HEX: ", end="")
    for i  in range(len(plaintext)):
        print(plaintext[i][2:], end=" ")
    print()
    print()

    n = len(plaintext)
    plaintextList = plaintTextToList(plaintext)

    

    # XOR with key
    def XORwithKey(pt,k):
        rangeTxt = int(n/nKey)
        t = []
        for j in range(nKey):
            t.append(hex(int(pt[j][2:],16) ^ int(k[j][2:],16)))
        return t

    # encryption!

    def encryption(roundNum, plaintext):   

        # substitute
        def byteSubstitution(plaintext):
            for i in range(nKey):
                b = BitVector(hexstring=plaintext[i][2:])
                int_val = b.intValue()
                s = Sbox[int_val]
                s = BitVector(intVal=s, size=8)
                plaintext[i] = "0x" + s.get_bitvector_in_hex()
                # print(s.get_bitvector_in_hex())
            return plaintext

        def stateMat(pw):
            pw = [ [] for i in range(4)] 
            for i in range(nKey):
                tmp =  i % 4
                pw[tmp].append(plaintext[i])
            return pw

        # shifting
        def shifting(pw):
            for i in range(4):
                pw[i] = list(pw[i][i:] + pw[i][:i]) 
            return pw
    
        
        plaintext = byteSubstitution(plaintext) 
        pw = stateMat(plaintext)
        pw = shifting(pw)




        # add round key
        tmpKey = keyList[roundNum + 1]
        

        def addRoundKey(pw,tmpKey):
            nextPT = []
            for i in range(4):
                for j in range(4):
                    nextPT.append(hex(int(pw[i][j][2:],16) ^ int(tmpKey[4*j + i][2:],16)))
            plaintext = nextPT
            return plaintext

        def mixColumn(pw):
            # import e extra jinis o ashe!!!
            mixer = [
                [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
                [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
                [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
                [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
            ]

            AES_modulus = BitVector(bitstring='100011011')


            # mix Column
            rowMixer = 4
            colPlaintext = 4
            colMixer = 4

            mixColResult = [[0 for i in range(4)] for j in range(4)]

            for i in range(rowMixer):
                for j in range(colPlaintext):
                    for k in range(colMixer):
                        bv1 = mixer[i][k]
                        bv2 = BitVector(hexstring=pw[k][j][2:])
                        bv = bv1.gf_multiply_modular(bv2, AES_modulus, 8)
                        mixColResult[i][j] = mixColResult[i][j] ^ int(bv)
            return mixColResult

        def mixColHex(mixColResult):
            for i in range(4):
                for j in range(4):
                    mixColResult[i][j] = hex(mixColResult[i][j])  
            return mixColResult
        
        def addRoundKeyMIX(mixColResult):
            nextPT = []
            for j in range(4):
                for i in range(4):
                    nextPT.append(hex(int(mixColResult[i][j][2:],16) ^ int(tmpKey[4*j + i][2:],16)))
            return nextPT
        
        
        if roundNum == 9:
            plaintext = addRoundKey(pw,tmpKey)

        else: 
            
            mixColResult = mixColumn(pw)
            mixColResult = mixColHex(mixColResult)
            plaintext = addRoundKeyMIX(mixColResult)            


        return plaintext

    cipherTextList = [['0x0']*16]

    for j in range(int(n/nKey)):
        plaintextList[j] = XORwithKey(plaintextList[j],cipherTextList[j])
        plaintextList[j] = XORwithKey(plaintextList[j],key)
        plaintext = plaintextList[j]

        for i in range(10):
            plaintext = encryption(i,plaintext)

        cipherText = ""

        temp = []
        for i in range(4):
            a = i
            while True:
                if a >= nKey:
                    break
                cipherText = cipherText + plaintext[a][2:] + " "
                temp.append(plaintext[a][:])
                a += 4
        cipherText = cipherText[:-1]
        cipherTextList.append(temp)

    print("Cipher Text: ")
    print("In HEX: ", end = "")   

    for i in range(1, len(cipherTextList)):
        for j in range(nKey):
            print(cipherTextList[i][j][2:], end= " ")
    print()
    print()

    print("In ASCII: ", end=" ")    
    cipherTextReturn = "" 
    for i in range(1, len(cipherTextList)):
        for j in range(nKey):
            cipherTextReturn += chr(int(cipherTextList[i][j][2:],16))
            print(chr(int(cipherTextList[i][j][2:],16)), end="")

    print()
    print()

    endTime = time.time()
    encryptTime = endTime - start

    return cipherTextReturn, keyGenTime, encryptTime
    
def decrypt(KEY,cipherTextReturn):
    # import hoynai!!
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



    # adding round constant
    def roundKey(key,roundNum):

        roundMat = ["0x01","0x02","0x04","0x08","0x10","0x20","0x40","0x80","0x1b","0x36"]
        w = [[] for i in range(4)]

        # XOR
        def XOR(a1,a2):
            temp = []
            n = len(a1)
            for i in range(n):
                temp.append(hex(int(a1[i][2:],16) ^ int(a2[i][2:],16)))
            return temp


        # creating state matrix
        def stateMatrix(key):
            for i in range(4):
                for j in range(4):
                    w[i].append(key[4*i+j])
            return w
        
        # circular bit shift
        def circularBitShift(w):
            return list(w[3][1:] + w[3][:1])
        
        # byte substitution
        def byteSubstitution(gw):
            for i in range(4):
                b = BitVector(hexstring=gw[i][2:])
                int_val = b.intValue()
                s = Sbox[int_val]
                s = BitVector(intVal=s, size=8)
                gw[i] = s.get_bitvector_in_hex()
                # print(s.get_bitvector_in_hex())
            return gw
        
        # adding round constant
        def addRoundConstant(gw):
            gw[0] = hex(int(gw[0],16) ^ int(roundMat[roundNum][2:],16))[2:]
            for i in range(4):
                gw[i] = "0x" + gw[i]
            return gw
        
        #new key generation
        def newKeyGen(w,gw):
            tempW = [w[i] for i in range(4)]
            tempW.append(gw)


            for i in range(4):
                tempW.append(XOR(tempW[i],tempW[i+4]))
            
            tempKey = []
            for i in range(5,9):
                for j in range(4):
                    tempKey.append(tempW[i][j])
            return tempKey

        w = stateMatrix(key)
        gw = circularBitShift(w)    
        gw = byteSubstitution(gw)
        gw = addRoundConstant(gw) 
        nextKey = newKeyGen(w,gw)

        return nextKey

    def keyGeneration(KEY):
        # round 0 key
        key = []
        for c in KEY:
            key.append(hex(ord(c)))

        tempList = []
        tempList.append(key)
        for i in range(1,11):
            tempList.append(roundKey(tempList[i - 1],i - 1))
        return tempList

    # given
    nKey = len(KEY)


    keyList = keyGeneration(KEY)


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


    key = keyList[10]
    n = len(cipherTextReturn)


    # XOR with key
    def XORwithKey(pt,k):
        rangeTxt = int(n/nKey)
        t = []
        for j in range(nKey):
            t.append(hex(int(pt[j][2:],16) ^ int(k[j][2:],16)))
        return t
    
    cipherTextList = [["0x0"]*16]
    i = 0
    while i < n:
        j = i
        temp = []
        for j in range(i, i+nKey):
            temp.append(hex(ord(cipherTextReturn[j])))
        cipherTextList.append(temp)
        i += nKey

    
    def decryption(roundNum,cipherText):
        key = keyList[roundNum]
    

        def stateMat(pw):
            pw = [ [] for i in range(4)] 
            for i in range(nKey):
                tmp =  i % 4
                pw[tmp].append(cipherText[i])
            return pw
        
        pw = stateMat(cipherText)

        # shifting
        def InvShifting(pw):
            for i in range(1,4):
                t = 4 - i
                pw[i] = list(pw[i][t:] + pw[i][:t]) 
            return pw

        pw = InvShifting(pw)

        # substitute
        def byteSubstitution(pw):
            for i in range(4):
                for j in range(4):
                    b = BitVector(hexstring=pw[i][j][2:])
                    int_val = b.intValue()
                    s = InvSbox[int_val]
                    s = BitVector(intVal=s, size=8)
                    pw[i][j] = "0x" + s.get_bitvector_in_hex()
                # print(s.get_bitvector_in_hex())
            return pw

        
        pw = byteSubstitution(pw) 


        tmpKey = keyList[roundNum]
        

        def addRoundKey(pw,tmpKey):
            for i in range(4):
                for j in range(4):
                    pw[i][j] = (hex(int(pw[i][j][2:],16) ^ int(tmpKey[4*j + i][2:],16)))
            return pw
            
        pw = addRoundKey(pw,tmpKey)


        if roundNum == 0:
            nextPt = []
            for i in range(4):
                for j in range(4):
                    nextPt.append(pw[j][i])
            return nextPt

        
        def mixColumn(pw):
            # import e extra jinis o ashe!!!
            InvMixer = [
                [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
                [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
                [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
                [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
            ]

            AES_modulus = BitVector(bitstring='100011011')


            # mix Column
            rowMixer = 4
            colPlaintext = 4
            colMixer = 4

            mixColResult = [[0 for i in range(4)] for j in range(4)]

            for i in range(rowMixer):
                for j in range(colPlaintext):
                    for k in range(colMixer):
                        bv1 = InvMixer[i][k]
                        bv2 = BitVector(hexstring=pw[k][j][2:])
                        bv = bv1.gf_multiply_modular(bv2, AES_modulus, 8)
                        mixColResult[i][j] = mixColResult[i][j] ^ int(bv)
            return mixColResult
        
        mixColRes = mixColumn(pw)

        def mixColHex(mixColResult):
            for i in range(4):
                for j in range(4):
                    mixColResult[i][j] = hex(mixColResult[i][j])  
            return mixColResult
        
        mixColRes = mixColHex(mixColRes)


        nextPT = []
        for j in range(4):
            for i in range(4):
                nextPT.append(mixColRes[i][j])
        return nextPT



    ptList = []

    for j in range(int(n/nKey)):
        cipherText = XORwithKey(cipherTextList[j + 1],key)

        for i in range(9,-1,-1):
            cipherText = decryption(i,cipherText)
        cipherText = XORwithKey(cipherTextList[j],cipherText)
        ptList.append(cipherText)



    print("Decipher Text: ")
    print("In HEX: ", end = "")    
    for i in range(len(ptList)):
        for j in range(nKey):
            print(ptList[i][j][2:], end= " ")
    print()
    print()

    print("In ASCII: ", end=" ")    

    decipherText = ""
    for i in range(len(ptList)):
        for j in range(nKey):
            decipherText += chr(int(ptList[i][j][2:],16))
            print(chr(int(ptList[i][j][2:],16)), end="")
    print()
    print()
    return decipherText

def main():
    KEY = "Thats my Kung Fu"
    PLAINTEXT = "Two One Nine Two"
    cipherTextReturn, keyGenTime, encryptionTime = encrypt(KEY,PLAINTEXT)

    start = time.time()
    
    decrypt(KEY,cipherTextReturn)
    
    endTime = time.time()
    decryptTime = endTime - start

    print("Execution Time Details: ")
    print("Key Schedule Time: ", keyGenTime * 1000, " ms")
    print("Encrypttion Time: ", encryptionTime * 1000, " ms")
    print("Decryption Time: ", decryptTime * 1000, " ms")


if __name__ == "__main__":
    main()