from Tkinter import *
import socket

s = socket.socket()
s.connect(('192.168.7.2', 1234))
def send_signal():
	s.send('Light On')

def light_off():
	s.send('Light Off')

root = Tk()
B = Button(root, text='Light On', command=send_signal)
Off = Button(root, text = 'Light Off', command = light_off)
B.pack()
Off.pack()
root.mainloop()
s.send('Close')
s.close()
