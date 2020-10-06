import rsa
import sys
import time

public_key_database = []
private_key_database = []
message_board = []
receivers = 0


#This function generates public private key pair for all the receivers
def setup(x):

    print("Initializing public key database. . ")
    for i in range(x):

        (pubkey, privkey) = rsa.newkeys(512)
        public_key_database.append(pubkey)
        print(pubkey)
        private_key_database.append(privkey)

    print ("Initialization complete")


#This function send an encrypted signal to a specific receiver and posts in the message board
def send(receiver):

    print("Sending encypted signal to receiver: " + str(receiver))

    publicKey = public_key_database[receiver]
    message = '1'.encode('utf8')
    encrypted = rsa.encrypt(message, publicKey)
    message_board.append(encrypted)

    print ("Signal passing complete")



#This function checks if a specific receiver has any signal in the message board
def receive(receiver):

    print("Looking up database for encypted signal for receiver: " + str(receiver))

    privateKey = private_key_database[receiver]
    messagecount = 0

    for m in message_board:
        try:
            message = rsa.decrypt(m, privateKey)
            if message.decode('utf8') == '1':
                messagecount += 1
        except:
            continue





    print ("Receiver "+ str(receiver)+ " has "+ str(messagecount)+ " messages")


if __name__ == "__main__":

    if len(sys.argv)<=1 :
        print ("Please specify number of receivers")
        exit(0)
    else:

        #Test code:
        receivers = int(sys.argv[1])
        print (receivers)
        setup(receivers)

        tic = time.perf_counter()

        send(1)
        receive(0)
        receive(1)

        toc = time.perf_counter()

        elapsed = toc-tic
        print("Elapsed time: "+str(elapsed) +" seconds")


