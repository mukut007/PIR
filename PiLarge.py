import random 
import rsa
import sys
import time


def server_setup(receivers, server_table_1,server_table_2,server_pubkeys,server_privkeys):
	(pubkey, privkey) = rsa.newkeys(512)
	server_pubkeys.append(pubkey)
	server_privkeys.append(privkey)
	(pubkey, privkey) = rsa.newkeys(512)
	server_pubkeys.append(pubkey)
	server_privkeys.append(privkey)

	server_table_1 = []
	server_table_2 = []

	return (server_table_1,server_table_2,server_pubkeys,server_privkeys)


def send(receiver,receivers):
	randomlist = random.sample(range(0,receivers-1), receivers//2)
	rflag = False
	if receiver in randomlist:
		rflag = True
	bin1 = [0]*receivers
	bin2 = [0]*receivers

	if rflag == True:
		for i in randomlist:
			bin1[i] = 1
			bin2[i] = 1
		bin2[receiver] = 0

	else:
		for i in randomlist:
			bin1[i] = 1
			bin2[i] = 1
		bin1[receiver] = 1
	slbin1 = [str(i) for i in bin1]
	sbin1 = "".join(slbin1)
	snum1 = str(int(sbin1, 2))
	slbin2 = [str(i) for i in bin2]
	sbin2 = "".join(slbin2)
	snum2 = str(int(sbin2, 2))
	signal = (rsa.encrypt(snum1.encode('utf8'), server_pubkeys[0]), rsa.encrypt(snum2.encode('utf8'), server_pubkeys[1]))
	return signal
	





def server_compute(server_number, message_board, server_table_1, server_table_2,receivers):
	for i in range(len(message_board)):

		enc_signal = message_board[i]
	
	
		signal = rsa.decrypt(enc_signal[server_number], server_privkeys[server_number])
		signal = signal.decode('utf8')
		signal = "{0:b}".format(int(signal))
		while(len(signal) != receivers):
			signal = "0" + signal
		print(signal)
		if server_number == 0:
			sboard_update = []
			# print (len(signal))
			print(len(server_table_1))
			if len(server_table_1) == 0:
				sboard_update = [int(x) for x in signal]
				server_table_1.append(sboard_update)
			else:
				for j in range(len(signal)):
					sboard_update.append(int(signal[j]) + int(server_table_1[i-1][j]))
				server_table_1.append(sboard_update)
		


		if server_number == 1:
			sboard_update = []
			if len(server_table_2) == 0:
				sboard_update = [int(x) for x in signal]

				server_table_2.append(sboard_update)
			else:
				for j in range(len(signal)):
					sboard_update.append(int(signal[j]) + int(server_table_2[i-1][j]))
				server_table_2.append(sboard_update)
	
	if server_number == 0:
		print(server_table_1)
		return server_table_1
	else:
		print(server_table_2)
		return server_table_2
		







def receive_helper(start, end, server_row_1,server_row_2,num_signals):
	ans = -1
	while start <= end:
		mid = (start + end)//2
		if server_row_1[mid] - server_row_2[mid] == num_signals:
			ans = mid
			end = mid - 1
		else: 
			start = mid + 1
	return ans
def receive(server_row_1, server_row_2):
	num_signals = server_row_1[-1] - server_row_2[-1] 
	signal_indices = []

	signal_index = receive_helper(0, len(server_row_1), server_row_1,server_row_2, num_signals )
	return signal_index


if __name__ == "__main__":

	message_board = []
	server_table_1 = []
	server_table_2 = []

	server_pubkeys = []
	server_privkeys = []
	if len(sys.argv)<=2 :
		print ("Please specify number of receivers and number of messages")
		exit(0)
	else:

        #Test code:
		receivers = int(sys.argv[1])
		messages = int(sys.argv[2])
		(server_table_1,server_table_2,server_pubkeys,server_privkeys) = server_setup(receivers,server_table_1,server_table_2,server_pubkeys,server_privkeys)
		tic = time.perf_counter()
		for i in range(messages):
			r = random.randint(0, receivers-1)
			signal = send(r,receivers)
			message_board.append(signal) 

		toc = time.perf_counter()
		sending = (toc - tic)/messages * 1000
		print("Message sending complete . . .\n\n\n")
		# print(server_table_1)
		print("Servers computing their tables")
		server_table_1 = server_compute(0,message_board, server_table_1, server_table_2,receivers)
		server_table_2 = server_compute(1,message_board, server_table_1, server_table_2,receivers)
		# print(server_table_1)
		print("Servers computing their tables done")


		tic = time.perf_counter()
		for i in range(receivers):
			srow1 = []
			srow2 = []

			for j in range(messages):
				srow1.append(server_table_1[j][i])
				srow2.append(server_table_2[j][i])
			receive(srow1,srow2)

		toc = time.perf_counter()
		receiving = (toc - tic) / receivers *1000

		print("Message receiving complete . . .\n\n\n")
		print("Average sending time: " + str(sending) + " miliseconds")
		print("Average receiving time: " + str(receiving) + " miliseconds")


