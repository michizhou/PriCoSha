from flask import Flask, request, render_template, json, session, redirect
from queryhelp import make_query, qh
from header import app
import defriend
import removegroups

@app.route('/friendGroups')
def friendGroups():
	if session.get('user'):
		return render_template('friendgroups.html')
	else:
		return render_template('signin.html', message="You haven't signed in yet!")

@app.route('/showAddFriendGroup')
def showAddFriendGroup():
	if session.get('user'):
		return render_template('showAddFriendGroup.html')
	else:
		return render_template('signin.html', message="You haven't signed in yet!")

@app.route('/addFriendGroup', methods=['POST'])
def addFriendGroup():
	try:
		if session.get('user'):
			#print("bloop")
			user = session.get('user')
			friendGroupName = request.form['friendGroup']
			friendGroupDes = request.form['friendGroupDes']
			query = "SELECT * FROM FriendGroup WHERE fg_name={}".format(qh(friendGroupName))
			if len(make_query(query, "q")) == 0:
				#print("bloop2")
				query='INSERT INTO FriendGroup VALUES({},{},{})'.format(qh(user),qh(friendGroupName),qh(friendGroupDes))
				queryBelong='INSERT INTO Belong VALUES({},{},{})'.format(qh(user),qh(user),qh(friendGroupName))
				if make_query(query, "i") == 0:
					name_str = friendGroupName
				else:
					return render_template('error.html', message = "An error occured")
				if make_query(queryBelong, "i") == 0:
					return render_template('friendgroups.html', name=name_str, message="has been added as a Friend Group!")
				else:
					return render_template('error.html', message = "An error occured")
			else:
				return render_template('showAddFriendGroup.html', message = "That FriendGroup already exists!")
		else:
			error = "Unauthorized Access"
			return render_template('error.html', error=error)
	except Exception as e:
		return render_template('error.html', error=str(e))

@app.route('/showAddFriend')
def showAddFriend():
	if session.get('user'):
		return render_template('showAddFriend.html')
	else:
		return render_template('signin.html', message="You haven't signed in yet!")

@app.route('/addFriend', methods=['POST'])
def addFriend():
	try:
		if session.get('user'):
			#print("bloop")
			user = session.get('user')
			friend = request.form['friend']
			friendGroup = request.form['friendGroup']
			query = "SELECT * FROM Person WHERE email={}".format(qh(friend))
			if friend != user:
				inFriendGroup = "SELECT friendgroup.owner_email, Friendgroup.fg_name FROM Friendgroup LEFT JOIN Belong ON Friendgroup.owner_email = Belong.owner_email AND Friendgroup.fg_name=Belong.fg_name WHERE (Friendgroup.fg_name={} AND email={}) OR (Friendgroup.fg_name={} AND friendgroup.owner_email={})".format(qh(friendGroup),qh(user), qh(friendGroup),qh(user))
				if len(make_query(inFriendGroup,"q"))>0:
					if len(make_query(query, "q")) > 0:
						checkAlreadyFriend = "SELECT * FROM Belong WHERE fg_name={} AND email={}".format(qh(friendGroup),qh(friend))
						if len(make_query(checkAlreadyFriend, "q")) == 0:
							query = 'INSERT INTO Belong VALUES({},{},{})'.format(qh(friend),qh(user),qh(friendGroup))
							if make_query(query, "i") == 0:
								queryDisplay = "SELECT fname FROM Person WHERE email={}".format(qh(friend))
								friendName = make_query(queryDisplay, "q")
								name_str = "{}".format(friendName[0]['fname'])
								return render_template('friendgroups.html', name=name_str, message="has been added to {}!".format(friendGroup))
							else:
								return render_template('error.html', message = "An error occured")
						else:
							return render_template('showAddFriend.html', message="They're already in that Friend Group!")
					else:
						return render_template('showAddFriend.html', message = "That person hasn't signed up yet!")
				else:
					return render_template('showAddFriend.html', message = "You're not in that Friend Group!")
			else:
				return render_template('showAddFriend.html', message ="You can't add yourself again!")
		else:
			error = "Unauthorized Access"
			return render_template('error.html', error=error)
	except Exception as e:
		return render_template('error.html', error=str(e))

@app.route('/getFriendGroups')
def getFriendGroups():
	try:
		if session.get('user'):
			user = session.get('user')
			query="SELECT fg_name, description FROM FriendGroup WHERE owner_email={}".format(qh(user))
			nameData = make_query(query, "q")
			return json.dumps(nameData)
		else:
			return render_template('signin.html', message = "You aren't signed in!")
	except Exception as e:
		return render_template('error.html', error=str(e))