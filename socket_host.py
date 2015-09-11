import socket

s = socket.socket()
host = '192.168.7.2'
port = 1234
s.bind((host, port))

s.listen(5)
c,a = s.accept()
print 'Got Connection from:',a
data = ''
while(data != 'Close'):
    c.send('Hello from Server')
    data =  c.recv(1024)
    print data   
   
c.close() 
