# http://www.bogotobogo.com/python/python_network_programming_server_client.php

# echo_client.py
import socket
import color
import os


KNOWN_HOSTS = [('atuin.optus.com.au',4747), ('10.123.0.94',4747), ('192.168.1.7',4747), ('192.168.1.11',4747), ('192.168.0.23',4747), ('192.168.0.26',4747), ('127.0.0.1',4747), ('localhost',4747)]


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
def connect(host, port):
	print "[*] Connecting to...", (host, port)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	print "[!] Connected to...", (host, port)
	return s

def connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print "[*] Connecting..."
	for h in KNOWN_HOSTS:
		try:
			print "[*] Connecting...", h
			#h = ('127.0.0.1', 4747)
			s.connect(h)
			print "[!]", color.OKGREEN + "Connected", h, color.ENDC
			return s
		except Exception as e:
			print "[!]", color.FAIL + str(e), h, color.ENDC
			pass
	print "[!]", color.FAIL + "Couldn't connect with any known host.", color.ENDC
	quit()


# Program
def main():
	welcome()
	# host, port = enter_host_port()
	# s = connect(host, port)
	s = connect()
	s.close()
	quit()


if __name__ == "__main__":
	main()
