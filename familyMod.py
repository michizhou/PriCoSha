from flask import Flask, request, render_template, json, session, redirect
from queryhelp import make_query, qh
from header import app

@app.route('/family')
def family():
	if session.get('user'):
		return render_template('listfamily.html')
	else:
		return render_template('signin.html', message="You haven't signed in yet!")
        
@app.route('/getFamily')
def getFamily():
	try:
		if session.get('user'):
			user = session.get('user')
			query="SELECT fname, lname FROM Person WHERE email IN (SELECT email_family FROM Family WHERE email={})".format(qh(user))
			nameData = make_query(query, "q")
			return json.dumps(nameData)
		else:
			return render_template('signin.html', message = "You aren't signed in!")
	except Exception as e:
		return render_template('error.html', error=str(e))
