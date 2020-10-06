import elgamal
import sys

#Create data bases for public keys, private keys, ciphertexts, message boards, and receivers
public_key_database = []
private_key_database = []
cipher_database = []
message_board = []
receivers = 0

#I use this implementation for guidance below
#https://github.com/RyanRiddle/elgamal/blob/master/README.md

#This function generates public private key pair for all the receivers
def setup(x):


    for i in range(x):
        #Generate public/private key pairs in a dictionary
        keys = elgamal.generate_keys()


        #Returns public and private keys and store in respective databases
        public_key_database.append(keys['publicKey'])
        private_key_database.append(keys['privateKey'])

    #Sample cipher code line
    #cipher = elgamal.encrypt(keys['publicKey'], "This is the message I want to encrypt")

    for key in public_key_database:
        #returns a cipher string with public keys and sample msg
        cipher = elgamal.encrypt(key, "This is the message I want to encrypt")

        #stores cipher texts in cipher data base
        cipher_database.append(cipher)

        #prints keys with respective cipher texts
        print(key, cipher, "\n")

    #This code is not part of the setup, just testing the decryption methods
    #for key1,ciphertxt in zip(private_key_database, cipher_database):
    #    plaintext = elgamal.decrypt(key1, ciphertxt)
    #    print(plaintext)


    print("Setup Initialization is complete")



if __name__ == "__main__":
    if len(sys.argv)<=1 :
            print ("Please specify number of receivers")
            exit(0)
    else:
        receivers = int(sys.argv[1])
        print (receivers)
        setup(receivers)
        #send(1)
        #receive(0)
        #receive(1)
