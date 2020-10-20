import elgamal
import sys
import time
import random

#Create data bases for public keys, private keys, ciphertexts, message boards, and receivers
public_key_database = []
private_key_database = []
cipher_database = []
sigma_database = []
message_board = []
receivers = 0
messages = 0

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
        cipher = elgamal.encrypt(key, '0')

        #stores cipher texts in cipher data base
        cipher_database.append(cipher)

        #prints keys with respective cipher texts
        print(key, cipher, "\n")

    #This code is not part of the setup, just testing the decryption methods
    #for key1,ciphertxt in zip(private_key_database, cipher_database):
    #    plaintext = elgamal.decrypt(key1, ciphertxt)
    #    print(plaintext)


    print("Setup Initialization is complete")

#This function send an encrypted signal to a specific receiver and posts in the message board
def send(receiver):
    print("Sending encypted signal to receiver: " + str(receiver))

    #Adding ciphertexts to message board
    for cipherMsg in cipher_database:
        message_board.append(cipherMsg)


    #Initialise Sigma values and encrypt them:
    iter = 0
    for key in public_key_database:
        if (iter == receiver):
            sigma = elgamal.encrypt(key, '1')
            sigma_database.append(sigma)

        else:
            sigma = elgamal.encrypt(key, '0')
            sigma_database.append(sigma)

        iter += 1


    #Compute C_m' and append to message board
    for (oldCipher, sigValue) in zip(cipher_database, sigma_database):
        new_cipher = oldCipher + sigValue
        message_board.append(new_cipher)
    #num = 0


#This function checks if a specific receiver has received a signal
def receive(receiver):

    #Initializing specific indexes of message board to values t and t_prime
    t = message_board[-1]
    t_key = private_key_database[-1]

    t_prime = message_board[receiver]
    t_primeKey = private_key_database[receiver]


    #Decrypting values at t and t_prime
    l = elgamal.decrypt(t_key, t)
    l_prime = elgamal.decrypt(t_primeKey, t_prime)


    #This is where I get problems(When doing the binary search to find whether t prime is the correct message/signal)
    #if float(l) - float(l_prime) == 0:

    #    print("message received", l_prime)
    #elif ((l - l_prime) > 0):

    # Also run step 2 (decryptig specific signals)
    #   t = t
    # t_prime = (t - t_prime) / 2
    #t = (t - t_prime) / 2)
    #t_prime = t


    print("Looking up database for encypted signal for receiver: " + str(receiver))
    #for msg in message_board:
    #    print("receive in progress")

if __name__ == "__main__":
    if len(sys.argv)<=2 :
            print ("Please specify number of receivers and messages")
            exit(0)
    else:
        receivers = int(sys.argv[1])
        messages = int(sys.argv[2])
        print (receivers)
        setup(receivers)

        tic = time.perf_counter()

        #for i in range(messages):
        r = random.randint(0, receivers-1)
        print("THIS IS R:", type(r))
        send(r)
        print("THIS IS R:", r)

        toc = time.perf_counter()
        sending = (toc - tic)/messages * 1000

        print("Message sending complete . . .\n\n\n")

        tic = time.perf_counter()
        #for i in range(receivers):

        receive(r)
        #receive(i)

        toc = time.perf_counter()
        receiving = (toc - tic) / receivers *1000

        #print("Message receiving complete . . .\n\n\n")
        #print("Average sending time: " + str(sending) + " miliseconds")
        #print("Average receiving time: " + str(receiving) + " miliseconds")
