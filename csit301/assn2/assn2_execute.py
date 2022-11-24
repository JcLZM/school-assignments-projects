#!/usr/bin/env python3

from Crypto.PublicKey import DSA
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
import binascii

#this program uses the scriptpubkey and scriptsig from the previous program
#to verify the signature of the message "Contemporary topic in security"
#for p2ms

#read scriptpubkey.txt
def read_scriptpubkey():
    f = open("scriptpubkey.txt", "r")
    scriptpubkey = f.read()
    f.close()
    return scriptpubkey

#read scriptsig.txt
def read_scriptsig():
    f = open("scriptsig.txt", "r")
    scriptsig = f.read()
    f.close()
    return scriptsig


#execute the scriptpubkey
def execute_scriptpubkey(scriptpubkey, scriptsig):
    #split the scriptpubkey into a list
    scriptpubkey_list = scriptpubkey.split(" ")
    #print(scriptpubkey_list)

    #get the number of keys
    script_m = scriptpubkey_list[0]
    #should read nubmer of sigs required
    script_m = int(script_m[-1])
    #convert to int holding no. of sigs
    #print(script_m)

    #get number of key
    script_n = scriptpubkey_list[-2]
    #convert to int holding no. of keys
    script_n = int(script_n[-1])

    #script_n = num of keys, script_m = num of sigs

    #get the keys
    keys = []
    for i in range(1, script_n+1):
        keys.append(scriptpubkey_list[i])
    #print(keys)

    #split the scriptsig into a list
    scriptsig_list = scriptsig.split(" ")
    
    #ignore op_1
    #get the sigs
    sigs = []
    for i in range(1, script_m+1):
        sigs.append(scriptsig_list[i])
    #print(sigs)

    #add stuff to stack
    stack = []
    for s in sigs:
        stack.append(s)
    stack.append(script_m)
    for k in keys:
        stack.append(k)
    stack.append(script_n)
    #print(stack)
    checkmultisig(stack)


def checkmultisig(stack):
    #reverses stack to verify
    stack.reverse()
    #retrieve first item (number of keys)
    numkeys = stack[0]
    stack.pop(0)
    #print(numkeys)
    keys = []
    for i in range(0, numkeys):
        keys.append(stack[0])
        stack.pop(0)
    
    #retrieve next item (number of sigs) required
    numsigs = stack[0]
    stack.pop(0)

    sigs = []
    for i in range(0, numsigs):
        sigs.append(stack[0])
        stack.pop(0)
    
    #read gpq from gpq.txt
    f = open("gpq.txt", "r")
    gpq = f.read()
    f.close()
    
    gpqsplit = gpq.split(" ")
    #print(gpq)
    g = gpqsplit[0]
    p = gpqsplit[1]
    q = gpqsplit[2]

    matches = 0
    for s in sigs:
        if keysverify(s, keys, g, p, q) == True:
            matches += 1
    
    if matches >= numsigs:
        #print("Transaction is valid")
        return 1
    else:
        return 0
    


def keysverify(sig, y, g, p, q):
    #y is a list of public keys
    #sig is 1 sig
    message = b"Contemporary topic in security"

    authenticmessage = False
    for k in y:
        #print(k)
        unhexedk = int(k, 16)
        #print(unhexedk)
        tup = [unhexedk, int(g), int(p), int(q)]
        #print(tup)
        key = DSA.construct(tup)
        verifier = DSS.new(key, 'fips-186-3')
        hash_obj = SHA256.new(message)
        try:
            verifier.verify(hash_obj, binascii.unhexlify(sig))
            #print("Signature is valid")
            authenticmessage = True
        except ValueError:
            print("Signature is not authentic")
    return authenticmessage

    


    

def main():
    #read scriptpubkey.txt and scriptsig.txt
    scriptpubkey = read_scriptpubkey()
    #has the format "OP_2 key1 key2 key3 key4 OP_4 OP_CHECKMULTISIG"
    scriptsig = read_scriptsig()
    #has the format "OP_1 sig1 sig2"
    if execute_scriptpubkey(scriptpubkey, scriptsig) == 1:
        print("Transaction is valid")
    else:
        print("Transaction is not valid")

    



if __name__ == '__main__': 
    main()