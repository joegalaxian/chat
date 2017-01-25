# http://www.bogotobogo.com/python/python_network_programming_server_client.php

# echo_server.py
import socket
import color
import os
import select

"""
host = ''	# Symbolic name meaning all available interfaces
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print "[*] Listening on...", (host,port)
s.listen(1)
conn, addr = s.accept()
print '[!] Connected', addr
while True:
	data = conn.recv(1024)
	if not data: break
	conn.sendall(data)
conn.close()
"""

KNOWN_HOSTS = [('atuin.optus.com.au',4747), ('10.123.0.94',4747), ('192.168.1.7',4747), ('192.168.1.11',4747), ('192.168.0.23',4747), ('192.168.0.26',4747), ('127.0.0.1',4747), ('localhost',4747)]


# Prints program tittle:
def welcome():
	os.system('clear')
	tittle = 'C H A T  -  S E R V E R'
	print tittle


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

EXIT_CODE = '/quitting'
# Main loop
def loop(s):
	hosts = []
	SOCKET_LIST = [s]
	while True:
		#select until socket modified
		ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [])
		
		# ready_to_read()
		for sock in ready_to_read:
			if sock == s:
				# new_connection()
				sockfd, addr = s.accept()
				SOCKET_LIST.append(sockfd)
				print "[+]", color.WARNING + "Connection", addr, color.ENDC
				#print '[>] DEBUG SOCKET_LIST', SOCKET_LIST
			else:
				# new_message()
				# Client message -> receive and broadcast (to all except server socket and sender socket).
				msg = sock.recv(1024)
				if msg != '':
					if msg == EXIT_CODE:
						# disconnection()
						print "[-]", color.WARNING + "Disconnection." + color.ENDC
						SOCKET_LIST.remove(sock)
						continue
					else:
						# broadcast()
						for host in SOCKET_LIST:
							if host != sock and host != s:
								#print "[>] DEBUG Sending '" +msg+ "' to ", host
								host.send(msg)

		# in_error()
		for sock in in_error:
			SOCKET_LIST.remove(sock)
			print "[!]", color.FAIL + "Socket in error.", sock, color.ENDC
			

# Creates socket, connects to known hosts, and listen 5.
def start():
	print "[*] Starting..."
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	for h in KNOWN_HOSTS:
		try:
			s.bind(h)
			print "[!]", color.OKGREEN + "Started at " + str(h) + color.ENDC
			s.listen(5)
			print "[*] Listening... (max 5)"
			return s
		except Exception as e:
			# print "[!]", color.FAIL + str(e), str(h) + color.ENDC
			pass


# Main program
def main():
	welcome()
	# host, port = enter_host_port()
	# s = get_socket(host,port)
	s = start()
	# listening(s)
	loop(s)
	s.close()


if __name__ == "__main__":
	main()
