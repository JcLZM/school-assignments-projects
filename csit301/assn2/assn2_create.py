#!/usr/bin/env python3

from Crypto.PublicKey import DSA
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
import binascii

#this program creates a scriptpublickey and a scriptsig for a 2 of 4 p2ms
#transaction


#Create a key
def create_key():
    key = DSA.generate(2048)
    return key

#create a key with fixed pqg
def create_key_fixedpqg(pqg):
    key = DSA.generate(2048, domain = pqg)
    return key

def create_scriptpubkey(key1, key2, key3, key4):
    #create the scriptpubkey
    #2 of 4 p2ms
    #convert to hex

    k1hex = hex(key1.y)
    k2hex = hex(key2.y)
    k3hex = hex(key3.y)
    k4hex = hex(key4.y)

    '''
    k1hex = binascii.hexlify(str(key1.y).encode("utf-8"))
    #print(k1hex)
    k2hex = binascii.hexlify(str(key2.y).encode("utf-8"))
    k3hex = binascii.hexlify(str(key3.y).encode("utf-8"))
    k4hex = binascii.hexlify(str(key4.y).encode("utf-8"))
    '''
    scriptpubkey = "OP_2 " + str(k1hex) + " " + str(k2hex) + " " + str(k3hex) + " " + str(k4hex) + " OP_4 OP_CHECKMULTISIG"
    return scriptpubkey

def sign_a_message(key):
    message = b"Contemporary topic in security"
    hash_obj = SHA256.new(message)
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(hash_obj)

    #print(hash_obj.hexdigest())
    #signature_hex = binascii.hexlify(signature)
    #print(signature_hex)
    return signature

def create_scriptsig(sig1, sig2):
    #convert bytes to hex
    #print(sig1)
    sig1hex = binascii.hexlify(sig1)
    sig2hex = binascii.hexlify(sig2)
    #sig1hex = sig1hex.decode("utf-8")
    #sig2hex = sig2hex.decode("utf-8")

    scriptsig = "OP_1 " + str(sig1hex) + " " + str(sig2hex)
    return scriptsig

def main():
#make 4 keys
    key1 = create_key()
    #print([key1.y, key1.p, key1.q, key1.g])
    tuple = [key1.p, key1.q, key1.g]
    #print(tuple)
    #rest of keys should use same pqg
    key2 = create_key_fixedpqg(tuple)
    key3 = create_key_fixedpqg(tuple)
    key4 = create_key_fixedpqg(tuple)

    #write scriptpubkey to file
    scriptpubkey = create_scriptpubkey(key1, key2, key3, key4)
    file = open("scriptPubKey.txt", "w")
    file.write(scriptpubkey)
    file.close()

    #also write gpq to file?
    file = open("gpq.txt", "w")
    gpq = str(key1.g) + " " + str(key1.p) + " " + str(key1.q)
    file.write(gpq)
    file.close()

    #sign a message
    sig1 = sign_a_message(key1)
    sig2 = sign_a_message(key3)
    scriptsig = create_scriptsig(sig1, sig2)
    #print(scriptsig)
    #write scriptsig
    file = open("scriptSig.txt", "w")
    file.write(scriptsig)
    file.close()
    #print(a)

if __name__ == '__main__': 
    main()