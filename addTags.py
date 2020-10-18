@app.route('/tagGroup', methods=['GET','POST'])
def tagGroup():
    userEmail = session.get('user')
    selectedContent = request.form.get('select_content')
    taggeeGroup = request.form['memGroup']
    conID = request.form['conID']
    cursor = conn.cursor()
    
    queryFindOwner = "SELECT group_owner_email FROM Belong WHERE member_email = %s AND group_name = %s"
    cursor.execute(queryFindOwner, (userEmail, taggeeGroup))
    ownerEmail = cursor.fetchall()
    
    queryGroupMembers = "SELECT member_email FROM Belong WHERE group_name = %s AND owner_email = %s"
    cursor.execute(queryGroupMembers, (taggeeGroup, ownerEmail))
    groupMembers = list(cursor.fetchall())
    
    for member in groupMembers:
        queryAlreadyTagged = "SELECT * FROM Tag JOIN Content ON Tag.id = Content.id WHERE content_name = %s AND Tag.username_taggee = %s"
        cursor.execute(queryAlreadyTagged, (selectedContent, member))
        data = cursor.fetchall()
        
        if not data:
            if(userEmail == member):
                querySendTag = "INSERT INTO Tag(id, username_tagger, username_taggee, status) VALUES(%s, %s, %s, %s)"
                cursor.execute(querySendTag, (conID, username, member, True))
                conn.commit()
                cursor.close()
                return redirect(url_for('tag'))

            else:
                querySendTag = "INSERT INTO Tag(id, username_tagger, username_taggee, status) VALUES(%s, %s, %s, %s)"
                cursor.execute(querySendTag, (conID, username, member, False))
                conn.commit()
                cursor.close()
                return redirect(url_for('tag'))
                