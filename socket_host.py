#!/usr/bin/python
import socket

#Function Definitios
def light_on():
	print 'Light On'

def light_off():
	print 'Lignt Off'

#Read Configuration file and save in configuration dictionary
#configuration contains key-value pair or different settings 
#with value in a form of list of strings
conf = open('socket_host.conf','r')       
configuration = {}
print 'Configurations:'
for line in conf:
	if(line[0] != '#'):
		line = line.split(':')
		configuration[line[0]] = line[1].strip().split(',')
		print line[0],':',configuration[line[0]]
print 

#Creates socket object and bind it to the server ip and port
#If the server_ip is not available server is created with localhost as ip
s = socket.socket()
host = configuration['server_ip'][0]
port = int(configuration['server_port'][0])
try:
	print 'Connecting to', host
	s.bind((host, port))
	print 'Server running at ' + host + ':' +str(port)
except socket.error:
	print 'Failed...'
	print 'Connecting to localhost'
	s.bind(('localhost',1234))
	print 'Server running at localhost' + ':' +str(port)
print 

#Server start listeing for connection from clients
s.listen(5)
c,a = s.accept()

#Check for any invlaid ip connection
if(a[0] in configuration['allowed_ip']):
	print 'Got Connection from:',a
	print 'Press Ctrl-C for exit'
	data = ''
	while(data != 'Close'):
		try:
			data =  c.recv(1024)
			if(data == 'Light On'):
				if(configuration['debug'] == 'true'):
					print 'Recieved Command -', data
				light_on()
			elif(data == 'Light Off'):
				if(configuration['debug'] == 'true'):
					print 'Recieved Command -', data
				light_off()
		except KeyboardInterrupt:
			break
	c.close() 
else:
	print 'Invalid IP connection request'
	c.close()

s.close()

