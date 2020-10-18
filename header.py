from flask import Flask, request, render_template, json, session, redirect
import pymysql.cursors
#from header import conn, app to use this module

conn = pymysql.connect(host='localhost',
						port=8889,
						user='root',
						password='root',
						db='PriCoSha',
						charset='utf8mb4',
						cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
app.secret_key = 'secret'