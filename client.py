# http://www.bogotobogo.com/python/python_network_programming_server_client.php

# echo_client.py
import color
import os
import sys
import socket
import select

KNOWN_HOSTS = [('atuin.optus.com.au',4747), ('192.168.1.7',4747), ('192.168.1.11',4747), ('192.168.0.23',4747), ('192.168.0.26',4747), ('127.0.0.1',4747), ('localhost',4747)]


""""
# host = socket.gethostname()
# host = 'atuin.optus.com.au'
host = '127.0.0.1'
port = 12345	# The same port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((host,port))
print "[*] Connecting to...", (host,port)
s.connect((host,port))
s.sendall(b'Hello, world')
data = s.recv(1024)
s.close()
print 'Received', repr(data)
"""

# Prints tittle
def welcome():
	os.system('clear')
	tittle = 'C H A T  -  C L I E N T'
	print tittle


# Enters host and port
def enter_host_port():
	host = raw_input("[*] Enter host (default '127.0.0.1'): ")
	if host == '':
		host = '127.0.0.1'

	port = raw_input("[*] Enter port (default 4747): ")
	if port == '':
		port = 4747
	else:
		port = int(port)

	return host, port


# Connects to the server
def connect2(host, port):
	print "[*] Connecting to...", (host, port)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	print "[!]", color.OKGREEN + "Connected to...", (host, port), color.ENDC
	return s


# manual_connect
def manual_connect():
	host, port = enter_host_port()
	return connect2(host, port)


# auto_connect
def auto_connect(host=None, port=None):
#if host == None and port == None:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	exception_stack = []
	print "[*] Connecting..."
	for h in KNOWN_HOSTS:
		try:
			# print "[i] DEBUG Connecting...", h
			s.connect(h)
			print "[!]", color.OKGREEN + "Connected", h, color.ENDC
			return s
		except Exception as e:
			# print "[>] DEBUG Error:", str(e)
			exception_stack.append("[!] " + color.FAIL + str(e) + " " + str(h) + color.ENDC)
			pass
	
	# Print exception stack and error.
	for e in exception_stack: print e
	print "[!]", color.FAIL + "Couldn't connect to any known host.", color.ENDC

	# manual_connect():
	return manual_connect()

#else: return connect(host, port)


EXIT_CODE = '/quitting'
# Terminates program after closing socket and optional printing.
def goodbye(sock = None, msg = None):
	if sock:
		sock.send(EXIT_CODE)
		sock.close()
	if msg: print msg
	quit()


# loop
def loop(s):
	SOCKET_LIST = [s, sys.stdin]
	name = raw_input("[*] Name: ")
	
	#prompt()
	sys.stdout.write(name + "> ")
	sys.stdout.flush()

	while True:

		#socket_select()
		ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [])

		#ready_to_read()
		for sock in ready_to_read:

			# server_message()
			if sock == s:
				# ()
				# Message from the server -> receive, print
				msg = s.recv(1024)
				
				#server_down()
				if not msg:
					goodbye(s, "\n[!] "+color.FAIL+"Disconnected from server."+color.ENDC)

				#print_message()
				sys.stdout.write('\r'+msg+'\n')
				sys.stdout.flush()

			# client_message()
			elif sock == sys.stdin:
				# User entered a chat -> send to server
				msg = sys.stdin.readline()
				msg = msg[:-1] #removes final '\n'
				if msg == '':
					#ignore
					continue
				elif msg == 'q':
					#disconnect and terminate
					goodbye(s, 'Quiting...')
				else:
					#send_message()
					msg = name + ": " + msg
					s.send(msg)

		""" TODO: IMPROVE
		#in_error()
		for sock in in_error:
			
			#server fail:
			if sock == s:
				print "[!]", color.FAIL+"Disconnected from server."+color.ENDC
				sock.close()
				quit()
		"""

		#prompt()
		sys.stdout.write(name + "> ")
		sys.stdout.flush()





# Program
def main():
	welcome()
	s = auto_connect()
	loop(s)
	goodbye(s, "[*] Program terminated.")


if __name__ == "__main__":
	main()
