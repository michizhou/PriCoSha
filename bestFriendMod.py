from flask import Flask, request, render_template, json, session, redirect
from queryhelp import make_query, qh
from header import app

@app.route('/bestFriends')
def bestFriends():
	if session.get('user'):
		return render_template('listbestfriends.html')
	else:
		return render_template('signin.html', message="You haven't signed in yet!")

@app.route('/showAddBestFriend')
def showAddBestFriend():
	if session.get('user'):
		return render_template('showAddBestFriend.html')
	else:
		return render_template('signin.html', message="You haven't signed in yet!")

@app.route('/addBestFriend', methods=['POST'])
def addBestFriend():
	try:
		if session.get('user'):
			bestieEmail = request.form['bestieEmail']
			checkExist = "SELECT * FROM Person WHERE email={}".format(qh(bestieEmail))
			user = session.get('user')
			if bestieEmail != user:
				if len(make_query(checkExist, "q"))>0:
					checkExistFriend="SELECT email FROM Friendgroup LEFT JOIN Belong ON Friendgroup.owner_email = Belong.owner_email AND Friendgroup.fg_name=Belong.fg_name WHERE email={} AND friendgroup.owner_email={}".format(qh(bestieEmail), qh(user))
					if len(make_query(checkExistFriend, "q"))>0:
						checkAlreadyBestie = "SELECT * FROM BestFriends WHERE email_bestie={} AND email={}".format(qh(bestieEmail),qh(user))
						if len(make_query(checkAlreadyBestie, "q")) == 0:
							query='INSERT INTO BestFriends VALUES({},{})'.format(qh(bestieEmail),qh(user))
							if make_query(query, "i") == 0:
								queryDisplay = "SELECT fname FROM Person WHERE email={} ".format(qh(bestieEmail))
								bestieName = make_query(queryDisplay, "q")
								name_str = "{}".format(bestieName[0]['fname'])
								return render_template('listbestfriends.html', name=name_str, message="has been added as your Best Friend!")
							else:
								return render_template('error.html', message = "An error occured")
						else:
							return render_template('showAddBestFriend.html', message="You are already Best Friends!")
					else:
						return render_template('showAddBestFriend.html', message="You aren't friends yet!")
				else:
					return render_template('showAddBestFriend.html', message = "That person hasn't signed up yet!")
			else:
				return render_template('showAddBestFriend.html', message ="You can't be Best Friends with yourself (although we do encourage self love <3)")
		else:
			error = "Unauthorized Access"
			return render_template('error.html', error=error)

	except Exception as e:
		return render_template('error.html', error=str(e))

@app.route('/showDeleteBestFriend')
def showDeleteBestFriend():
	if session.get('user'):
		return render_template('showDeleteBestFriend.html')
	else:
		return render_template('signin.html', message="You haven't signed in yet!")


@app.route('/deleteBestFriend', methods=['POST'])
def deleteBestFriend():
	try:
		if session.get('user'):
			user=session.get('user')
			bestieEmail = request.form['bestieEmail']
			checkExist = "SELECT * FROM Person WHERE email={}".format(qh(bestieEmail))
			if user != bestieEmail:
				if len(make_query(checkExist, "q")) > 0:
					checkIfBestie = "SELECT * FROM BestFriends WHERE email_bestie={} AND email={}".format(qh(bestieEmail),qh(user))
					if len(make_query(checkIfBestie, "q")) != 0:
						query='DELETE FROM BestFriends WHERE email={} AND email_bestie={}'.format(qh(user),qh(bestieEmail))
						if make_query(query, "i") == 0:
							queryDisplay = "SELECT fname FROM Person WHERE email={}".format(qh(bestieEmail))
							bestieName = make_query(queryDisplay, "q")
							name_str = "{}".format(bestieName[0]['fname'])
							return render_template('listbestfriends.html', name=name_str, message="has been removed from your Best Friends")
						else:
							return render_template('error.html', message = "An error occured")
					else:
						return render_template('showAddBestFriend.html', message="You aren't Best Friends!")
				else:
					return render_template('showAddBestFriend.html', message = "That person hasn't signed up yet!")
			else:
				return render_template('showAddBestFriend.html', message = "You can't delete yourself!")
		else:
			error = "Unauthorized Access"
			return render_template('error.html', error=error)
	except Exception as e:
		return render_template('error.html', error=str(e))		

@app.route('/getBestFriends')
def getBestFriends():
	try:
		if session.get('user'):
			user = session.get('user')
			query="SELECT fname, lname FROM Person WHERE email IN (SELECT email_bestie FROM BestFriends WHERE email={})".format(qh(user))
			nameData = make_query(query, "q")
			return json.dumps(nameData)
		else:
			return render_template('signin.html', message = "You aren't signed in!")
	except Exception as e:
		return render_template('error.html', error=str(e))
