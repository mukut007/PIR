import random 
import rsa
import sys
import time
import paillier

def server_setup(receivers, server_table_1,server_table_2,server_pubkeys,server_privkeys):
	(pubkey, privkey) = rsa.newkeys(3072)
	server_pubkeys.append(pubkey)
	server_privkeys.append(privkey)
	(pubkey, privkey) = rsa.newkeys(3072)
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
	
		# signal = server_privkeys[server_number].decrypt(enc_signal[server_number])
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
		







def receive_helper(lo, hi, server_row_1,server_row_2,num_signals,signal_indices):
	# ans = -1
	# init_lo = start
	# init_hi = end
	# while start <= end:
	# 	mid = (start + end)//2
	# 	if server_row_1[mid] - server_row_2[mid] == num_signals:
	# 		ans = mid
	# 		end = mid - 1
	# 	else: 
	# 		start = mid + 1
	# signal_indices.append(ans)
	# num_signals = (server_row_1[ans-1] - server_row_2[ans-1]) - (server_row_1[init_lo] - server_row_2[init_lo]) 
	# if num_signals != 0:
	# 	receive_helper(init_lo, ans-1,server_row_1,server_row_2, num_signals,signal_indices  )
	# num_signals = (server_row_1[init_hi] - server_row_2[init_hi]) - (server_row_1[ans + 1] - server_row_2[ans + 1]) 
	# if num_signals != 0:
	# 	receive_helper(ans+1, init_hi,server_row_1,server_row_2, num_signals,signal_indices )
	# print("hi",hi)
	# print(lo)
	if hi <= lo :
		# print("no more signals here")
		return 

	# print(hi)
	# print(lo)

	num_signals = (server_row_1[hi] - server_row_2[hi]) - (server_row_1[lo] - server_row_2[lo]) 
	if num_signals == 0:
		# print ("NO MORE SIGNALS")
		return
	else:   
		init_lo = lo
		init_hi = hi
        # print (lo)
        # print (hi)
		while lo <= hi:
			mid = (lo + hi)//2
            # print (mid)
			if (server_row_1[mid] - server_row_2[mid]) - (server_row_1[init_lo] - server_row_2[init_lo])   == num_signals:
                # print("here")
                # ans = mid
				hi = mid - 1
			else: 
				lo = mid +1

		# print(lo)
		signal_indices.append(lo)
		if lo > 0 and (server_row_1[lo-1] - server_row_2[lo-1]) - (server_row_1[init_lo] - server_row_2[init_lo]) > 0:	
			receive_helper(init_lo, lo - 1,server_row_1,server_row_2, num_signals, signal_indices)
		elif lo < len(server_row_1)-1 and (server_row_1[init_hi] - server_row_2[init_hi]) - (server_row_1[lo+1 ] - server_row_2[lo+1]) > 0:
			receive_helper(lo + 1, init_hi,server_row_1,server_row_2, num_signals, signal_indices) 
		return
def receive(server_row_1, server_row_2):
	num_signals = server_row_1[-1] - server_row_2[-1] 
	signal_indices = []

	receive_helper(0, len(server_row_1)-1, server_row_1,server_row_2, num_signals,signal_indices )
	print(signal_indices)
	# return signal_indices


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
		tic = time.perf_counter()

		server_table_1 = server_compute(0,message_board, server_table_1, server_table_2,receivers)
		server_table_2 = server_compute(1,message_board, server_table_1, server_table_2,receivers)
		# print(server_table_1)
		print("Servers computing their tables done")
		toc = time.perf_counter()
		server_time = (toc - tic)/messages * 1000
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
		print("Average sending time: " + str(sending) + " milliseconds")
		print("Average receiving time: " + str(receiving) + " milliseconds")
		print("Average server computation time : " +  str(server_time) + "milliseconds")


