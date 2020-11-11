import elgamal
import sys
import time
import random
import operator
import textwrap
from functools import reduce

#Create data bases for public keys, private keys, ciphertexts, message boards, and receivers
Rec_public_key_database = []
Rec_private_key_database = []
Receiver_database = []
#sigma_database = []
message_board = []
CM_board = []
recList = []
ReceivedBoard = []
receivers = 0
messages = 0

#I use this implementation for guidance below
#https://github.com/RyanRiddle/elgamal/blob/master/README.md

#This function generates public private key pair for all the receivers
#def setup(receivers, Rec_public_key_database, Rec_private_key_database, Receiver_database):
def setup(receivers):

    for i in range(receivers):
        #Generate public/private key pairs in a dictionary
        keys = elgamal.generate_keys()


        #Returns public and private keys and store in respective databases
        Rec_public_key_database.append(keys['publicKey'])
        Rec_private_key_database.append(keys['privateKey'])


    for key in Rec_public_key_database:
        #returns a cipher string with public keys and sample msg
        cipher = elgamal.encrypt(key, '0')

        #stores cipher texts in cipher data base
        Receiver_database.append(cipher)

        #prints keys with respective cipher texts
        print("key = ", key, "cipher= ", cipher, "\n")



    print("Setup Initialization is complete")

#This function send an encrypted signal to a specific receiver and posts in the message board
def send(receiver, receivers):
    print("Sending encypted signal to receiver: " + str(receiver))



    #Initialise Signal values and encrypt them:
    sigma_database = []
    iter = 0
    sing = ["0"] * receivers
    singi = ' '

    print("THIS IS RECEIVER: ", receiver)

    for key in Rec_public_key_database:
        #Compute signal value with Enc(1) for k = i
        if (iter == receiver):
        #if (receiver in randomlist):
            sigma = elgamal.encrypt(key, '1')

            sigma_database.append(sigma)

        else:
            #Compute signal value with Enc(0) for k not equal i
            sigma = elgamal.encrypt(key, '0')

            sigma_database.append(sigma)

        iter += 1
    signal = singi.join(sigma_database)

    message_board.append(sigma_database)




def computeCMboard(messages, receivers):
    sigList = []

    for val in message_board:
        if isinstance(val, list):
            sigList.append(val)

    RecNum = 0
    for element in sigList:

        RecNum = len(element)

    long = len(sigList)
    TotSig = ''
    CM_list = []
    shortList = []
    wholeList = []
    whop = ''
    t_matrix = zip(*sigList)
    for row in t_matrix:

        CM_list.append(row)

    message_board.append(CM_list)


def sumColumn(Llist, column):
    total = 0
    M_list = []
    new_list = []
    cip_list = []
    num = 0
    for line in Llist:

        for key, cip in zip(Rec_private_key_database, line):
            plain = elgamal.decrypt(key, cip)
            cip_list.append(plain)


        new_list.append(cip_list)
        cip_list = []

    for row2 in new_list:
        row2 = [int(i) for i in row2]
        M_list.append(row2)
    for row in range(len(M_list)):
        total += M_list[row][column]
    return total

def DecryptBoard(receivers):
    m_list = []
    for key, cipherttff in zip(Rec_private_key_database, message_board[:receivers]):
        plainwork = elgamal.decrypt(key, cipherttff)
        m_list.append(plainwork)
        #ReceivedBoard.append(plainwork)
    ReceivedBoard.append(m_list)
    print("All zeros: ", ReceivedBoard)

    sigList = []
    signal = ''
    temp_list = []
    for line in message_board[receivers:-1]:

        for key, cip in zip(Rec_private_key_database, line):

            plainwap = elgamal.decrypt(key, cip)
            temp_list.append(plainwap)
        ReceivedBoard.append(temp_list)
        temp_list = []
    print("All zeros AND some hmm: ", ReceivedBoard)

    CMboard = message_board[-1]
    temp_list = []
    L_matrix = zip(*CMboard)
    for row1 in L_matrix:
        temp_list.append(row1)
    temp_tot = 0
    lister = []

    for i in range(len(temp_list)):
        temp_tot = sumColumn(temp_list, i)
        lister.append(temp_tot)
    print(lister)
    ReceivedBoard.append(lister)
    print("All zeros plus som hmmm and the BANG!!: ", ReceivedBoard)

def receive_helper(start, end, lastCheckSig,num_signals):

    ans = -1

    if num_signals == 0:
        print("No signals")
    else:
        while start <= end:
            mid = (start + end) // 2
            if ((lastCheckSig[mid] > 0) and (lastCheckSig[mid + 1] > 0)):

                end = mid - 1

            elif ((lastCheckSig[mid] == 0) and (lastCheckSig[mid + 1] > 0)):
                ans = mid
                #print("Did we get HEre????")

                break
            elif ((lastCheckSig[mid] == 0) and (lastCheckSig[mid + 1] == 0)):
                start = mid + 1

    return(ans)

#This function checks if a specific receiver has received a signal
def receive(receiver):
    #print("yet")
    CM = ReceivedBoard[-1]
    num_signals = CM[receiver]

    transList = []
    t_matrix = zip(*ReceivedBoard)
    lastCheckSig = []
    for row in t_matrix:
        transList.append(row)
    checkSigList = transList[receiver]
    for i in checkSigList:
        val = int(i)
        lastCheckSig.append(val)
    print("What is it: ", lastCheckSig)
    signal_index = receive_helper(0, len(ReceivedBoard), lastCheckSig, num_signals )
    print("This is it...", signal_index + 1)
    signal_index = 0

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

        #Adding cipher messages to message board
        for cipherMsg in Receiver_database:
            message_board.append(cipherMsg)

        for i in range(messages):
            r = random.randint(0, receivers-1)
            recList.append(r)
            print("THIS IS R:", r)
            send(r, receivers)

        computeCMboard(messages, receivers)

        num4 = 0
        for line in message_board:
            num4 += 1
            #print("closely examine: ", line)
        print("fourth: ", num4)


        toc = time.perf_counter()
        sending = (toc - tic)/messages * 1000

        print("Message sending complete . . .\n\n\n")

        tic = time.perf_counter()


        decryptedBoard = []
        DecryptBoard(receivers)
        for i in range(receivers):
            receive(i)


        toc = time.perf_counter()
        receiving = (toc - tic) / receivers *1000

        #print("Message receiving complete . . .\n\n\n")
        #print("Average sending time: " + str(sending) + " miliseconds")
        #print("Average receiving time: " + str(receiving) + " miliseconds")
