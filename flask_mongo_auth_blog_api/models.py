## models come inherit the db class so we inherit from them
from __main__ import db 


## if you type from app import db then
## a recursion will create app import db
## tthem model import app and so on so in this 
## file use __main__

#from app import db
## import only when you try to migrate
## only and only when you migrate 
## comment the from __main__ import db
## then un comment it and then comment this 

from datetime import datetime

class User(db.Model):
	## you must declare a primary key
	## otherwise no foreigh key
	id = db.Column(db.Integer,primary_key = True)
	username = db.Column(db.String(100),index=True,unique=True)
	email = db.Column(db.String(100),index=True,unique = True)
	password_hash = db.Column(db.String(200))
	## add the foregin key
	## part one here
	posts = db.relationship('Post',backref='author',lazy = 'dynamic')
## adding the elation ship with other shcema

class Post(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	body = db.Column(db.String(200))
	timestamp = db.Column(db.DateTime,index=True,default = datetime.utcnow)
	## this is part of the foreign 
	## part two add here 
	## thats why we need the foreign key
	## and the name will be 'user' not 'User'
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))


