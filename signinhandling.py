from flask import Flask, request, render_template, json, session, redirect
from queryhelp import make_query, qh
from header import app

@app.route('/authenticateUser', methods=['POST'])
def authenticateUser():
	try:
		username = request.form['username']
		password = request.form['password']
		query2 = 'SELECT email, password FROM Person WHERE email={} AND password=sha2({},256)'.format(qh(username), qh(password))
		data = make_query(query2,"q")
		if len(data) > 0:
			session['user'] = data[0]['email']
			user=session.get('user')
			query = "SELECT fname FROM Person WHERE email={}".format(qh(user))
			name = make_query(query, "q")
			name_str = "{}".format(name[0]['fname'])
			return render_template('userHome.html',name=name_str)
		else:
			error = "Email and/or Password is wrong or doesn't exist"
			return render_template('signin.html', message=error)
	except Exception as e:
		return render_template('error.html', error=str(e))

@app.route('/showLogIn')
def login():
	if session.get('user'):
		return redirect('/userHome')
	else:
		return render_template('signin.html')

@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')

@app.route('/logout')
def logout():
	session.pop('user',None)
	message = "Successfully logged out!"
	return render_template('index.html', message=message)

@app.route('/signUp', methods=['POST'])
def signUp():
	username = request.form['new_username']
	password = request.form['new_password']
	fname = request.form['fname']
	lname = request.form['lname']
	query = 'SELECT * FROM Person WHERE email = {}'.format(qh(username))
	data = make_query(query, "q")
	if (data):
		error  = 'User already exists!'
		return render_template('signup.html', message=error)
	else:
		insert = 'INSERT INTO Person VALUES({},sha2({},256),{},{})'.format(qh(username),qh(password),qh(fname),qh(lname))
		make_query(insert, "i")
		return render_template('signin.html', message="Sign up success! Now you can log in.")


