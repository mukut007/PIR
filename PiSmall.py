# import elgamal
import sys
import time
import random
import operator
import textwrap
from phe import paillier
from functools import reduce




# public_key, private_key = paillier.generate_paillier_keypair()

# # Add 1 to a small positive number
# ciphertext1 = public_key.encrypt(15)
# ciphertext2 = public_key.encrypt(1)
# ciphertext3 = ciphertext1 + ciphertext2
# decryption = private_key.decrypt(ciphertext3)
# print(decryption)

#Create data bases for public keys, private keys, ciphertexts, message boards, and receivers
Rec_public_key_database = []
Rec_private_key_database = []
Receiver_database = []
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
        public_key, private_key = paillier.generate_paillier_keypair()


        #Returns public and private keys and store in respective databases
        Rec_public_key_database.append(public_key)
        Rec_private_key_database.append(private_key)

    init_counters = []
    for key in Rec_public_key_database:
        #returns a cipher string with public keys and sample msg
        init_counter_key = key.encrypt(0)

        #stores cipher texts in cipher data base
        init_counters.append(init_counter_key)
    message_board.append(init_counters)

        #prints keys with respective cipher texts
        # print("key = ", key, "cipher= ", cipher, "\n")



    print("Setup Initialization is complete")

#This function send an encrypted signal to a specific receiver and posts in the message board
def send(receiver, receivers):
    print("Sending encypted signal to receiver: " + str(receiver))



    #Initialise Signal values and encrypt them:
    sigma_database = []
    iter = 0

    # print("THIS IS RECEIVER: ", receiver)
    signal = []
    for key in Rec_public_key_database:
        #Compute signal value with Enc(1) for k = i
        if (iter == receiver):
        #if (receiver in randomlist):
            sigma = key.encrypt(1)

            # sigma_database.append(sigma)

        else:
            #Compute signal value with Enc(0) for k not equal i
            sigma = key.encrypt(0)

            # sigma_database.append(sigma)
        signal.append(message_board[-1][iter] + sigma )

        iter += 1


    message_board.append(signal)



def bin_search(receiver, lo, hi, signal_indices):
    if hi <= lo:
        # print("no more signals here")
        return 
    num_signals = Rec_private_key_database[receiver].decrypt(message_board[hi][receiver]) - Rec_private_key_database[receiver].decrypt(message_board[lo][receiver]) 
    if num_signals == 0:
        # print ("NO MORE SIGNALS")
        return
        # return
    # print(lo)
    else:   
        init_lo = lo
        init_hi = hi
        # print (lo)
        # print (hi)
        while lo <= hi:
            mid = (lo + hi)//2
            # print (mid)
            if Rec_private_key_database[receiver].decrypt(message_board[mid][receiver]) == num_signals:
                # print("here")
                # ans = mid
                hi = mid - 1
            else: 
                lo = mid + 1

        
        signal_indices.append(lo)
        bin_search(receiver, init_lo, lo - 1, signal_indices)
        bin_search(receiver, lo + 1, init_hi, signal_indices) 
        return


def receive(receiver):
    # num_signals = Rec_private_key_database[receiver].decrypt(message_board[-1][receiver])
    # print(num_signals)
    signal_indices = []

    bin_search(receiver, 0, len(message_board)-1, signal_indices)
    


    return signal_indices

#Function to compute the Values for the CM Values (Sending section bullets 3-4)
# def computeCMboard(messages, receivers):
#     #Create a list to store the signals in the message board
#     sigList = []

#     for val in message_board:
#         if isinstance(val, list):
#             sigList.append(val)

#     #Create a list to store the computed CM Values
#     CM_list = []

#     #Collect each respective receiver's signals and then store them as a list for each receiver. This is how I compute the CM values for each receiver and store them for later.

#     t_matrix = zip(*sigList)
#     for row in t_matrix:

#         CM_list.append(row)
#     #The CM values for each receiver are then appended to the message board and stored for each receiver. THis will then be used to decrypt and find the number of signals for a respective receiver.
#     message_board.append(CM_list)

# #This is a function to decrypt the values of the encrypted signals and CM values for a respective receiver. It is called in the receive functions for both signal and CM values right below.
# def RecSigExtract(item, receiver, Trans_SigList):
#     #Decrypts a signal/CM value for respective receiver
#     plaintext = elgamal.decrypt(Rec_private_key_database[receiver], item)

#     #Returns that plaintext
#     return(plaintext)

# #Function to decrypt a receiver's original counter... This will always decrypt to zero for each receiver.
# def TrueReceiveMsg(receivers, receiver):
#     RecSpecificList = []
#     msg_list = []
#     #Simply decrypts a receiver's original counter before any signals were sent.
#     for msg in message_board[:receivers]:
#         msg_list.append(msg)
#     plaintext = elgamal.decrypt(Rec_private_key_database[receiver], msg_list[receiver])

#     return(plaintext)

# #Function to decrypt all of a receiver's respective signals
# def TrueReceiveSignals(receivers, receiver):

#     signal_list = []
#     Trans_SigList = []
#     #Collects all of the signals for all receivers and simply transposes this nested list into a format that allows me to collect a receiver's respective signals
#     for signal in message_board[receivers:-1]:
#         signal_list.append(signal)
#     S_matrix = zip(*signal_list)
#     for row1 in S_matrix:
#         Trans_SigList.append(row1)

#     Decrypt_list = []
#     #Runs the function above with a receiver's respective signal values to decrypt those values and return them
#     for item in Trans_SigList[receiver]:

#         dec = RecSigExtract(item, receiver, Trans_SigList)

#         Decrypt_list.append(dec)

#     return(Decrypt_list)

# #Function to decrypt all of a receiver's respective CM values
# def TrueReceiveCM(receivers, receiver):
#     t = message_board[-1]
#     CM_list = []
#     #Run the function above to decrypt the respective CM values for a receivers. Should be a list of the total signals that each receiver received.
#     for item in t[receiver]:
#         dec = RecSigExtract(item, receiver, t)
#         CM_list.append(dec)
#     #Returns this list back
#     return(CM_list)

# #This function takes the decrypted msgs, signals, and CM values for a respective user and then performs the binary search to find the total number of counter updates for a message.
# def TrueReceiveSearch(SpecificReceiveList):

#     #I do not collect the original counter values since they are not needed to search. They will all be zero anyways. I collect all the signal values and CM values for a receiver only

#     #These next several lines of code I simply convert the values for signals and CM values into integers and append them to a flat list.
#     sig = SpecificReceiveList[1]
#     SigIntList = []
#     print("Is it always middle??: ", type(sig))
#     for line1 in sig:
#         newline1 = int(line1)
#         SigIntList.append(newline1)

#     print("integers for my signals??: ", SigIntList)
#     print("Are these lists correct?", SpecificReceiveList)
#     CMintList = []
#     CMsig = SpecificReceiveList[-1]
#     for line in CMsig:
#         print("a list?!?!", line)
#         newline = int(line)
#         CMintList.append(newline)
#     print("int list plllsss: ", CMintList)
#     num_signals = sum(CMintList)
#     print("correct Sum?: ", num_signals)

#     #This is where I formulate my flat list. The list of the signal values and sum of singals for a respective user.
#     SigIntList.append(num_signals)
#     print("SAAAYYY IT AIINNT SOOOO: ", SigIntList)

# def receive_helper(start, end, lastCheckSig,num_signals):

#     ans = -1

#     if num_signals == 0:
#         print("No signals")
#     else:
#         while start <= end:
#             mid = (start + end) // 2
#             if ((lastCheckSig[mid] > 0) and (lastCheckSig[mid + 1] > 0)):

#                 end = mid - 1

#             elif ((lastCheckSig[mid] == 0) and (lastCheckSig[mid + 1] > 0)):
#                 ans = mid
#                 #print("Did we get HEre????")

#                 break
#             elif ((lastCheckSig[mid] == 0) and (lastCheckSig[mid + 1] == 0)):
#                 start = mid + 1

#     return(ans)


if __name__ == "__main__":
    if len(sys.argv)<=2 :
            print ("Please specify number of receivers and messages")
            exit(0)
    else:
        receivers = int(sys.argv[1])
        messages = int(sys.argv[2])
        # print (receivers)

        setup(receivers)

        tic = time.perf_counter()

        #Adding cipher messages to message board
        # for cipherMsg in Receiver_database:
        #     message_board.append(cipherMsg)
        # print(message_board)
        for i in range(messages):
            r = random.randint(0, receivers-1)
            recList.append(r)
            # print("THIS IS R:", r)
            # print("Index is ", i)
            send(r, receivers)

        # computeCMboard(messages, receivers)

        toc = time.perf_counter()
        sending = ((toc - tic) * 1000)/messages

        print("Message sending complete . . .\n\n\n")

        tic = time.perf_counter()
        # print(message_board)
        for i in range(receivers):
            #Create a list that will store a receiver's respective decrypted signals, and CM values which will be used to search for their updated counters in TrueReceiveSearch().
            # SpecificReceiveList = []
            # bruh = TrueReceiveMsg(receivers, i)
            # SpecificReceiveList.append(bruh)
            # yes = TrueReceiveSignals(receivers, i)
            # SpecificReceiveList.append(yes)
            # tough = TrueReceiveCM(receivers, i)
            # SpecificReceiveList.append(tough)
            # print("Is this correct?", SpecificReceiveList)
            # TrueReceiveSearch(SpecificReceiveList)
            print("Receiver", i)
            print("Indices are : ", receive(i))
            # receive(i)

        toc = time.perf_counter()
        receiving = ((toc - tic) * 1000)/receivers



        print("Message receiving complete . . .\n\n\n")
        print("Average sending time: " + str(sending))
        print("Average receiving time: " + str(receiving))
