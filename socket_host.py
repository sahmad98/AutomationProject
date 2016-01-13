#!/usr/bin/python
import socket
import sqlite3
import hashlib
import sys
import getpass

#Function Definitios
def light_on():
	print 'Light On'

def light_off():
	print 'Lignt Off'

def authenticate(username, passward):
	pass_hash = hashlib.sha256(passward)
	db = sqlite3.connect('logins')
	try:
		cur = db.cursor()
		query = "select username,name from users where passward='"+pass_hash.hexdigest()+"';"
		cur.execute(query)
		result = cur.fetchall()
		if(len(result) != 1):
			print 'Username or Passward Incorrect!'
			db.close()
			return False
		elif(len(result) == 1 and result[0][0] == username):
			db.close()
			print 'Welcome back!, '+result[0][1]
			return True
		else:
			db.close()
			print 'Username or Passward Incorrect!'
			return False
	except sqlite3.OperationalError as e:
		print e
		db.close()
		return False
	except IndexError as e:
		print 'User with username '+username+' not found.'
		return False

welcome = '''
--------------------------------------------
    Welcome to Home Automation Server
--------------------------------------------

created by: Saleem Ahmad
GitHub: @sahmad98
____________________________________________
'''

print welcome
#Authentication of User
try:
	user = raw_input('Username: ')
	pwd = getpass.getpass()
except KeyboardInterrupt:
	print
	sys.exit(-1)
if(not authenticate(user, pwd)):
	sys.exit(-1)

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
try:
	c,a = s.accept()
except KeyboardInterrupt:
	print 'Closing down server'
	s.close()
	sys.exit()

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

