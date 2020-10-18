from flask import Flask, request, render_template, json, session, redirect
from header import app

@app.route('/removeFriendGroup', methods=['POST'])
def removeFriendGroup():
    userEmail = session.get('user')
    friendGroupName = request.form['groupName']
    mFirstName = request.form['memfname']
    mLastName = request.form['memlname']
    cursor = conn.cursor()
    
    # Delete friend group only after we have ensured that 
    # person we want to remove from the group exists
    queryFindMemUserEmail = "SELECT email FROM Person WHERE first_name = %s AND last_name = %s"
    cursor.execute(queryFindMemUserEmail, (mFirstName, mLastName))
    memUserEmail = cursor.fetchone().get('email')
     
    # Delete from friend group only after we have ensured that 
    # person we want to remove from the group is in the group
    queryFindMembership = "SELECT group_owner_email FROM Belong WHERE group_name = %s AND member_email = %s"
    cursor.execute(queryFindMembership, (friendGroupName, memUserEmail))
    groupOwnerEmail = cursor.fetchone().get('group_owner_email')
    
    # Ensure that the group to which member wants to be removed from
    # is actually owned by the owner of the group
    queryFindGroup = "SELECT * FROM Friendgroup WHERE group_name = %s AND owner_email = %s"
    query_results = cursor.execute(queryFindGroup, (friendGroupName, groupOwnerEmail))
    
    # Remove yourself from the group
    if query_results:     
        queryMeQuit = "DELETE FROM Belong WHERE group_name = %s AND owner_email = %s AND member_email = %s"
        cursor.execute(queryMeQuit, (friendGroupName, groupOwnerEmail, memUserEmail))
    conn.commit()
    cursor.close()
    return redirect(url_for('friends'))