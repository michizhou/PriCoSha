from flask import Flask, request, render_template, json, session, redirect
from queryhelp import make_query, qh
from header import app

@app.route('/showTagPeople')
def showTagPeople(error=""):
	if session.get('user'):
		user = session.get('user')
		queryMyContent = "SELECT item_name, item_id FROM ContentItem WHERE email_post = %s" % qh(user)
		data = make_query(queryMyContent, "q")
		return render_template('tag.html', contentItems=data, message=error)
	else:
		return render_template('signin.html', message="You haven't signed in yet!")

@app.route('/tagPeople', methods=['POST'])
def tagPeople():
	if session.get('user'):
		username = session.get('user')
		taggeeUsername = request.form['memUsername']
		conID = request.form['select_content']
		print(conID)
		if conID == "Select One":
			error="You must select an option"
			return showTagPeople(error)
		else:
			# conID = request.form['conID']

			queryAlreadyTagged = "SELECT * FROM Tag NATURAL JOIN ContentItem WHERE item_id = {} AND  email_tagged = {}".format(qh(conID),qh(taggeeUsername))
			data = make_query(queryAlreadyTagged, "q")

			if(data):
				error = "This person was already invited"
				return render_template('tag.html', message=error)

			elif(username == taggeeUsername):
				return render_template('tag.html', message="You can't tag yourself")

			else:
				querySendTag = "INSERT INTO Tag(email_tagged, email_tagger, item_id, status) VALUES({}, {}, {}, {})".format(qh(taggeeUsername),qh(username),int(conID), qh("pending"))
				make_query(querySendTag,"i")
				return render_template('userHome.html', message="Tag sent")
	else:
		return render_template('signin.html', message="You haven't signed in yet!")

@app.route('/viewTags')
def viewTags():
	if session.get('user'):
		username = session.get('user')

		queryPending = "SELECT email_tagger, item_name, file_path, status FROM Tag NATURAL JOIN ContentItem WHERE email_tagged = {} AND status = 'pending'".format(qh(username))
		pendingData = make_query(queryPending, "q")
		queryAccepted = "SELECT email_tagger, item_name, file_path, status FROM Tag NATURAL JOIN ContentItem WHERE email_tagged = {} AND status = 'accepted'".format(qh(username))
		acceptedData = make_query(queryAccepted, "q")
		return render_template('acceptTag.html', tagAcceptedData=acceptedData, tagDeclinedData=pendingData)


@app.route('/tagDecline', methods=['GET','POST'])
def tagDecline():
	username = session['username']
	selectedContent = request.form.get('select_content')
	conID = request.form['conID']
	cursor = conn.cursor();

	deleteTag = "DELETE FROM Tag WHERE username_taggee = %s AND id = %s"
	cursor.execute(deleteTag, (username, conID))
	conn.commit()
	cursor.close()
	return redirect(url_for('viewTags'))

@app.route('/tagAccept', methods=['GET','POST'])
def tagAccept():
	username = session['username']
	selectedContent = request.form.get('select_content')
	conID = request.form['conID']
	cursor = conn.cursor();

	queryUpdateTag = "UPDATE Tag SET status = %s WHERE username_taggee = %s AND id = %s"
	cursor.execute(queryUpdateTag, (True, username, conID))
	conn.commit()
	cursor.close()
	return redirect(url_for('viewTags'))
