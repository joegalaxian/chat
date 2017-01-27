# http://www.bogotobogo.com/python/python_network_programming_server_client.php

import socket
import os
import color
import select

LISTEN_MAX	= 10
KNOWN_HOSTS	= [('atuin.optus.com.au',4747), ('10.123.0.94',4747)]
LOCAL_HOST	= [('127.0.0.1',4747), ('localhost',4747)]
EXIT_CODE	= '/quitting'

# Network IP constructor (192.168.1.1:4747/192.168.255.255:4747).
def network():
	for i in range(256):
		for j in range(256):
			yield ('192.168.%d.%d' % (i,j), 4747)

# Prints program tittle:
def welcome():
	os.system('clear')
	tittle = 'C H A T  -  S E R V E R'
	print tittle

# Terminates program after closing socket and optional printing.
def goodbye(sock = None, msg = None):
	if sock:
		sock.send(EXIT_CODE)
		sock.close()
	if msg: print msg
	quit()

# Creates socket, connect, and listen 5.
def start():
	try:
		print "[*] Starting..."
		s = connect(KNOWN_HOSTS + list(network()) + LOCAL_HOST)
		return s
	except Exception as e:
		goodbye(None, "[!]" + color.FAIL + " Error: " + str(e) + color.ENDC)

# Creates, connects, listen and return socket if successfull, or None if unsuccessfull.
def connect(host_list):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	for h in host_list:
		try:
			# print "[>] DEBUG Connecting to...", h
			s.bind(h)
			print "[!]", color.OKGREEN + "Started at " + str(h) + color.ENDC
			s.listen(LISTEN_MAX)
			print "[*] Listening... (max %d)" % LISTEN_MAX
			return s
		except Exception as e:
			# print "[>] DEBUG " + str(e)
			pass
	raise Exception("Couldn't connect.")

# Main loop
def loop(s):
	hosts = []
	SOCKET_LIST = [s]
	while True:
		#socket_select()
		ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [])
		# ready_to_read()
		for sock in ready_to_read:
			# new_connection()
			if sock == s:
				sockfd, addr = s.accept()
				SOCKET_LIST.append(sockfd)
				print "[+]", color.WARNING + "Connection", addr, color.ENDC
				#print '[>] DEBUG SOCKET_LIST', SOCKET_LIST
			else:
				#new_message()
				# Client message -> receive and broadcast (to all except server socket and sender socket).
				msg = sock.recv(1024)
				if not msg:
					# client_down()
					print "[-]", color.WARNING+"Disconnection.", sock.getpeername(), color.ENDC
					SOCKET_LIST.remove(sock)
					continue
				elif msg != '':
					# disconnection()
					if msg == EXIT_CODE:
						print "[-]", color.WARNING+"Disconnection.", sock.getpeername(), color.ENDC
						SOCKET_LIST.remove(sock)
						continue
					# broadcast()
					else:
						for host in SOCKET_LIST:
							if host != sock and host != s:
								#print "[>] DEBUG Sending '" +msg+ "' to ", host
								host.send(msg)
		# in_error()
		for sock in in_error:
			SOCKET_LIST.remove(sock)
			print "[!]", color.FAIL + "Socket in error.", sock, color.ENDC

"""
# Enter host and port
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

# Binds socket
def get_socket(host, port):
	try:
		print "[*] Getting socket...", (host, port)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		print "[!] Socket bound."
		return s
	except Exception as e:
		print "[!] Error:", str(e)
		s.close()
		quit()

# Listening
def listening(s):
	i = raw_input("[*] Enter max host number (default 5): ")
	if i == '':
		i = 5
	else:
		i = int(i)
	s.listen(i)
	print "[!] Listening (max " + str(i) + ")..."
"""

# Main program
def main():
	welcome()
	# host, port = enter_host_port()
	# s = get_socket(host,port)
	server_socket = start()
	loop(server_socket)
	goodbye(server_socket)

if __name__ == "__main__":
	main()
