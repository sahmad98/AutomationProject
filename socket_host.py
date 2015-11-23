#!/usr/bin/python
import socket

conf = open('socket_host.conf','r')       
configuration = {}
for line in conf:
	if(line[0] != '#'):
		line = line.split(':')
		configuration[line[0]] = line[1].strip().split(',')

print configuration
s = socket.socket()
host = '192.168.7.2'
port = 1234
try:
	s.bind((host, port))
	print 'Server running at ' + host + ':' +str(port)
except socket.error:
	s.bind(('localhost',1234))
	print 'Server running at localhost' + ':' +str(port)

s.listen(5)
c,a = s.accept()
print a
if(a[0] in configuration['allowed_ip']):
	print 'Got Connection from:',a
	print 'Press Ctrl-C for exit'
	data = ''
	while(data != 'Close'):
		try:
			data =  c.recv(1024)
			print data
		except KeyboardIterrupt:
	c.close() 

else:
	print 'Invalid IP connection request'
	c.close()
s.close()

