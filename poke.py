from flask import Flask, request, render_template, json, session, redirect
from header import app
from queryhelp import make_query, qh

import pymysql.cursors

@app.route('/showPoke')
def showPoke():
	if session.get('user'):
		return render_template('listpokes.html')
	else:
		return render_template('signin.html', message="You haven't signed in yet!")

@app.route("/poke")
def poke():
	if session.get('user'):
		anEmail = session.get('user')
		#print("bug")
		toBePoked = request.form['toBePoked']
		#print("bug2")
		query = "SELECT 'fname','lname' FROM person WHERE 'email' = {}".format(qh(anEmail))
		data = make_query(query)
		if len(data)>0:
			message = "You poked {} {}".format(data[0]['fname'], data[0]['lname'])                       
			return render_template('showPoke.html', message=message)
		else:
			return render_template('error.html', error="query failed")
	else:
		return render_template('signin.html', message="You haven't signed in yet!")