import rsa
import sys
import time
import random
from phe import paillier
public_key_database = []
private_key_database = []
message_board = []
receivers = 0
messages = 0


#This function generates public private key pair for all the receivers
def setup(x):

    print("Initializing public key database. . ")
    for i in range(x):

        (pubkey, privkey) = paillier.generate_paillier_keypair()
        public_key_database.append(pubkey)
        # print(pubkey)
        private_key_database.append(privkey)

    #time.sleep(10)
    print ("Initialization complete")


#This function send an encrypted signal to a specific receiver and posts in the message board
def send(receiver):

    print("Sending encypted signal to receiver: " + str(receiver))

    publicKey = public_key_database[receiver]
    # message = '1'.encode('utf8')
    # encrypted = rsa.encrypt(message, publicKey)
    encrypted = publicKey.encrypt(1)
    message_board.append(encrypted)

    print ("Signal passing complete")



#This function counts how many signals a specific receiver has in the message board
def count_message(receiver):

    print("Looking up database for encypted signal for receiver: " + str(receiver))

    privateKey = private_key_database[receiver]
    messagecount = 0

    for m in message_board:
        try:
            message = privateKey.decrypt(m)
            if message == 1:
                messagecount += 1
        except:
            continue

    print ("Receiver "+ str(receiver)+ " has "+ str(messagecount)+ " messages")


#This function checks if a specific receiver has any signal in the message board
def receive(receiver):

    print("Looking up database for encypted signal for receiver: " + str(receiver))

    privateKey = private_key_database[receiver]
    messagecount = 0

    for m in message_board:

        try:
            message = privateKey.decrypt(m)
            if message == 1:
                print ("Message retrieved for receiver "+ str(receiver))
                messagecount += 1
                


        except:

            continue

        if (messagecount == 0) :
            print("Receiver " + str(receiver) + " has " + str(messagecount) + " messages")




if __name__ == "__main__":

    if len(sys.argv)<=2 :
        print ("Please specify number of receivers and number of messages")
        exit(0)
    else:

        #Test code:
        receivers = int(sys.argv[1])
        messages = int(sys.argv[2])
        print (receivers)
        setup(receivers)

        tic = time.perf_counter()

        for i in range(messages):

            r = random.randint(0, receivers-1)
            send(r)

        toc = time.perf_counter()
        sending = (toc - tic)/messages * 1000

        print("Message sending complete . . .\n\n\n")


        tic = time.perf_counter()
        for i in range(receivers):

            receive(i)

        toc = time.perf_counter()
        receiving = (toc - tic) / receivers *1000

        print("Message receiving complete . . .\n\n\n")
        print("Average sending time: " + str(sending) + " miliseconds")
        print("Average receiving time: " + str(receiving) + " miliseconds")






