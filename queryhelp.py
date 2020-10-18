from flask import Flask, render_template
import pymysql.cursors
from header import conn

def make_query(query, s):
#connects to server and formats queries (subject to change soon
#because of additional server procedure yet to be added)
	cursor = conn.cursor()
	#search
	if s == "q":
		#print("zloop")
		cursor.execute(query)
		#print("zloop2")
		return cursor.fetchall()
	#insert into table return 0 if success, -1 otherwise
	elif s == "i":
		cursor.execute(query)
		if len(cursor.fetchall()) is 0:
			conn.commit()
			cursor.close()
			return 0
		else:
			return -1

def qh(s):
	#formats strings for ease of use in queries
	return "\'" + s + "\'"