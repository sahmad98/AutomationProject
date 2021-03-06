#!/usr/bin/python

from Tkinter import *
import socket
import sys

s = socket.socket()
args = sys.argv

if(len(args) >= 2):
	try:
		print 'Connecting to', args[1]
		s.connect((args[1], 1234))   #Connects bealgebone on 1234 Port
		print 'Connected'
	except socket.error as e:
		print e
else:
	try:
		print 'Connecting to 192.168.7.2'
		s.connect(('192.168.7.2',1234))
		print 'Connected'
	except socket.error as e:
		print e

def light_on():
	try:
		s.send('Light On')
	except socket.error as e:
		print e

def light_off():
	try:
		s.send('Light Off')
	except socket.error as e:
		print e

root = Tk()  	

Button_on = Button(root, text='Light On', command=light_on)
Button_off = Button(root, text = 'Light Off', command = light_off)
Button_on.pack()
Button_off.pack()

root.mainloop()
try:
	s.send('Close')
except socket.error as e:
	print e

s.close()
