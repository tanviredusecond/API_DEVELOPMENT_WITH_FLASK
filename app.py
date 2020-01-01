
## --------------------------------------------
#importts for the web api
from flask import Flask,jsonify,request
from flask_restful import Api,Resource 
from pymongo import MongoClient
import bcrypt 
import requests
import subprocess
import json 
from pprint import pprint
#-----------------------------------------------


# The main building block provided by Flask-RESTful are resources.
# Resources are built on top of Flask pluggable views, giving you
# easy access to multiple HTTP methods just by defining methods on
# your resource. A basic CRUD resource for a todo application
# (of course) looks like this:
# the resources allow you use the get post put and delete method
# with their name



#-----------------------------------------------
def check_connection(client):
    if client:
        print("connection established")
    else:
        print ("connection failed")    



def UserExists(username):
    if users.find({"username":username}).count()==0:
        return False
    else:
        return True

#------------------------------------------------



## declare an app
app = Flask(__name__) ## it will create a flask object
## declare for the api
api = Api(app)      ## it will create a restfull api object

## connect to the mongodatabase
client = MongoClient("mongodb://localhost:27017")
check_connection(client);
## select the database
db = client.ImageRecognition
print(db)

#-----------------------------------------------------
## this is the user part

# creating ollection inside the database
users = db['users']  ## this is for storing users


class Register(Resource):

    ## create a Post request
    def post(self):
        ## get all the posted data
        ## get the json value
        posteddata = request.get_json()
        ## we need to parse the username and password
        username = posteddata['username']
        password = posteddata['password']
        
        ## if user exists then error 301
        if UserExists(username):
            ## prepare a json
            response = {
                "status":301,
                "msg":"invalid username"
            }
            return jsonify(response)

        ## if it is not the case
        ## that means the user is new so tae the hased password
        hashed_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
        ## making the hashed password
        ## now store the user and the password inthe database
        users.insert({
            "username":username,
            "password":hashed_pw,
            "Tokens":4
        })
        ## data isn inserted
        ## return the success messgae
        response = {
            "status": 200,
            "msg": "successfully Registered"
        }
        return jsonify(response)

class GetAllTheUsers(Resource):
    def get(self):
        all_users = list(users.find({}))
        return jsonify(json.dumps(all_users,default=str))


api.add_resource(Register,'/register')
api.add_resource(GetAllTheUsers,'/get_all_users')

if __name__ == '__main__':
    app.run(debug=True)