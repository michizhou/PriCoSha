from flask import Flask, request, render_template, json, session, redirect
from header import app

@app.route('/addComment', methods=['GET','POST'])
def add_comments():
    userEmail = session.get('user')
    selectedContent = request.form.get('select_content')
    commentToBeAdded = request.form.get('comment')
    cursor = conn.cursor()
    
    # Check that content item is visible to user
    queryFindOwner = "SELECT item_id, is_pub FROM ContentItem WHERE item_name = %s"
    cursor.execute(queryFindOwner, (selectedContent))
    isPublic = cursor.fetchone().get('is_pub')
    conID = cursor.fetchone().get('item_id')
    
    queryFriendGroups = "SELECT * FROM Belong NATURAL JOIN Share WHERE member_email = %s AND item_id = %s"
    cursor.execute(queryFriendGroups, (userEmail, conID))
    groupExists = cursor.fetchall()
    
    if isPublic or groupExists:
        # Inserts comment information into comments table of database
        queryAddComment = "INSERT INTO Comments(email, item_id, comment) VALUES (%s, %s, %s)"
        cursor.execute(queryAddComment, (userEmail, conID, commentToBeAdded))
