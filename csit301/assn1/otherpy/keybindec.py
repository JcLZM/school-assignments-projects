#!/usr/bin/env python3

#this script decrypts key.bin using ransomprvkey.pem (RSA encryption)
#and then decrypts the encrypted files using the key
#and then renames the files from .enc to .txt

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

file_in = open("key.bin", "rb")
private_key = RSA.import_key(open("ransomprvkey.pem").read())
enc_data = file_in.read(private_key.size_in_bytes())
cipher_rsa = PKCS1_OAEP.new(private_key)

key = cipher_rsa.decrypt(enc_data)
print(key)
file_in.close()

file_out = open("key.txt", "wb")
file_out.write(key)
file_out.close()