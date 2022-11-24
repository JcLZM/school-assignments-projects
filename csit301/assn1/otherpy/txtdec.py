#!/usr/bin/env python3

#decrypts files and renames from .enc to .txt
#decryption first - 

#IV is first line, Ciphertext is second line, key is key.txt

from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
import glob, os


for item in glob.glob("*.enc"):
    Filein = open(item, 'rb')
    iv = Filein.readline()
    ciphertext = Filein.readline()
    key = open('key.txt', 'rb')
    key_bytes = key.read()
    key.close()
    print(pad(key_bytes, 32))
    cipher = AES.new(pad(key_bytes,32), AES.MODE_CBC, b64decode(iv))
    plaintext = unpad(cipher.decrypt(b64decode(ciphertext)), AES.block_size)
    
    Filein.close()
    Fileout = open(item, 'w')
    Fileout.write(plaintext.decode('utf-8'))
    Fileout.close()
    os.rename(item, item[:-4] + '.txt')
