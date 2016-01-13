#!/usr/bin/python

#Finally this file should be compiled and made into an 
#executable using freeze so that no changes into code can be done.
import sqlite3
import os
import sys
import hashlib
import getpass

if os.getuid() != 0:
	print 'Reqire administrative privilages.'
	sys.exit(-1)

welcome = '''
-------------------------------------------------------------
Welcome to Registration Service of Bealgebone Home Automation
-------------------------------------------------------------
Created by: Saleem Ahmad
GitHub: @sahmad98

Type help - For help about different topics
For creating a new user Type create [name] [username]
'''

def createNewUser(name, username, passward):
	db = sqlite3.connect('logins')
	cur = db.cursor()
	try:
		pwd = hashlib.sha256(passward)
		query = "select * from users where username='"+username+"';"
		cur.execute(query)
		result = cur.fetchall()
		if(len(result) > 0):
			print "Username already exits."
			return
		query = "insert into users values('" + name + "', '" + username + "', '" + pwd.hexdigest() + "');"
		print query
		cur.execute(query)
		db.commit()
	except sqlite3.OperationalError as e:
		print e
		cur.execute("create table users(name text, username text, passward text);")
		query = "insert into users values('" + name + "', '" + username + "', '" + pwd.hexdigest() + "');"
		print query
		cur.execute(query)
		db.commit()
	finally:
		db.close()

def getUserList():
	db = sqlite3.connect('logins')
	cur = db.cursor()
	try:
		query = "select name from users;"
		print query
		cur.execute(query)
		for result in cur.fetchall():
			print result
	except sqlite3.OperationalError as e:
		print e
	finally:
		db.close()

def deleteUser(username):
	db = sqlite3.connect('logins')
	cur = db.cursor()
	try:
		query = "delete from users where username='" + username + "';"
		print query
		cur.execute(query)
		db.commit()
	except sqlite3.OperationalError as e:
		print e
	finally:
		db.close()

print welcome
command = ['']
op = ''
while(op != 'exit'):
	print 'server>>>', 
	command = raw_input()

	command = command.split()
	if(len(command) > 0):
		op = command[0]
		if(op == 'create'):
			if(len(command) != 3):
				print "2 arguments needed - [name] [username]"
			else:
				pwd = getpass.getpass()
				createNewUser(command[1], command[2], pwd)
		elif(op == 'users'):
			getUserList()
		elif(op == 'delete'):
			if(len(command) !=2):
				print "please enter username -- delete [username]"
			else:
				deleteUser(command[1])
