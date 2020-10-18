from flask import Flask, request, render_template, json, session, redirect
from queryhelp import make_query, qh
from header import app
import signinhandling
import content
import friendgroups
import bestFriendMod
import tags
import poke
import familyMod
import comments

import pymysql.cursors

@app.route('/userHome')
def userHome():
	if session.get('user'):
		user=session.get('user')
		query = "SELECT fname FROM Person WHERE email={}".format(qh(user))
		name = make_query(query, "q")
		name_str = "{}".format(name[0]['fname'])
		return render_template('userHome.html', name=name_str)
	else:
		return render_template('signin.html', message="You aren't signed in!")

@app.route("/")
def main():
	if session.get('user'):
		user = session.get('user')
		return render_template('index.html', message="User {} is still signed in, click Log In to continue the session or to reach the Log Out button".format(user))
	else:
		return render_template('index.html')

if __name__ == "__main__":
	app.run()
