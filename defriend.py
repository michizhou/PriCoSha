from flask import Flask, request, render_template, json, session, redirect
from header import app

@app.route('/defriend', methods=['POST'])
def defriend():
    if session.get('user'):
        userEmail = session.get('user')
        mFirstName = request.form.get('memfname')
        mLastName = request.form.get('memlname')
        cursor = conn.cursor()
        
        # Defriend user only after we have ensured that person
        # we want to remove from all user groups exists
        queryFindMemUserEmail = "SELECT email FROM Person WHERE first_name = %s AND last_name = %s"
        cursor.execute(queryFindMemUserEmail, (mFirstName, mLastName))
        memUserEmail = cursor.fetchone().get('email')
        
        # Check that defriended user is in a friend group of defriending user
        queryFindFormerMember = "SELECT * FROM Belong WHERE group_owner_email = %s AND member_email = %s"
        cursor.execute(queryFindFormerMember, (userEmail, memUserEmail))
        queryReturn = cursor.fetchall()
        
        if queryReturn:
            # Delete defriended user from friend groups owned by defriending user
            queryRevokeFriend = "DELETE FROM Belong WHERE group_owner_email = %s AND member_email = %s"
            cursor.execute(queryRevokeFriend, (userEmail, memUserEmail))
            
            # Delete defriended user from friend groups owned by defriending user
            queryRevokeTags = "DELETE FROM Tag WHERE tagger_email = %s AND taggee_email = %s"
            cursor.execute(queryRevokeTags, (userEmail, memUserEmail))
        
        conn.commit()
        cursor.close()
        return redirect(url_for('friends'))
    else:
        return render_template('signin.html', message="You haven't signed in yet!")
