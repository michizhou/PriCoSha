from flask import Flask, request, render_template, json, session, redirect
from queryhelp import make_query, qh
from header import app
from comments import add_comments
import datetime

@app.route('/showAddContent')
def showAddContent():
	if session.get('user'):
		return render_template('makenewpost.html')
	else:
		return render_template('signin.html', message="You haven't signed in yet!")

@app.route('/addContent', methods=['POST'])
def addContent():
	try:
		if session.get('user'):
			postTitle = request.form['title']
			postBody = request.form['body']
			try: #i'm pretty sure there's a better way to deal w this
				isPublic = request.form['public']
			except Exception:
				isPublic = 0
			email = session.get('user')
			query='INSERT INTO ContentItem(email_post, file_path, item_name, is_pub) VALUES({},{},{},{})'.format(qh(email), qh(postBody), qh(postTitle), isPublic)
			if make_query(query, "i") == 0:
				return render_template('userHome.html', message="Your content has been posted")
			else:
				return redirect('showAddContent.html', message = "An error occured") 
		else:
			error = "Unauthorized Access"
			return render_template('error.html', error=error)

	except Exception as e:
		return render_template('error.html', error=str(e))

@app.route('/getContent')
def getContent():
	try:
		if session.get('user'):
			user = session.get('user')
			data=[]
			bestieQuery = "SELECT fname, lname, item_name, file_path, post_time FROM ContentItem NATURAL JOIN Person WHERE email=email_post AND email IN (SELECT email_bestie FROM BestFriends WHERE email={})".format(qh(user))
			bestieData = make_query(bestieQuery, "q")
			if len(bestieData) > 0:
				bestieData.reverse()
				for item in bestieData:
					data.append(item)
			genQuery = "SELECT fname, lname, item_name, file_path, post_time FROM ContentItem NATURAL JOIN Person WHERE email=email_post AND email NOT IN (SELECT email_bestie FROM BestFriends WHERE email={})".format(qh(user))
			genData = make_query(genQuery, "q")
			#print(genData)
			if len(genData) > 0:
				genData.reverse()
				for item in genData:
					data.append(item)
			#print(data)
			return json.dumps(data)
		else:
			return render_template('signin.html', message = "You aren't signed in!")
	except Exception as e:
		return render_template('error.html', error=str(e))

@app.route('/getPublicContent')
def getPublicContent():
	try:
		if session.get('user'):
			return getContent()
		else:
			time = datetime.datetime.now()
			one_day = datetime.timedelta(days=1)
			query="SELECT fname, lname, item_name, file_path, post_time FROM ContentItem NATURAL JOIN Person WHERE email=email_post AND is_pub=1"
			data = make_query(query, "q")
			count = 0
			try:
				while count < len(data):
					row=data[count]
					count+=1
					remainder_time = time-row['post_time']
					if remainder_time >= one_day:
						data.remove(row)
						count-=1
			except Exception as e:
				return render_template('error.html', error=str(e))
			data.reverse()
			return json.dumps(data)
	except Exception as e:
		return render_template('error.html', error=str(e))

