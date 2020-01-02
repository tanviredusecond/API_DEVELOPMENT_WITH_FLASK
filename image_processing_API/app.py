
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



def gendict(status,msg):
    response = {
        "status":status,
        "msg":msg
    }
    return response

def verify_pw(username,password):
    if not UserExists(username):
        return False
    hashed_pw = users.find({
        "username":username
    })[0]["password"]

    ## decode the password
    ## and match
    ## the thing that you type vs that which is 
    ## found in the database
    if bcrypt.hashpw(password.encode('utf8'),hashed_pw)== hashed_pw:
        return True
    else:
        return False


def verifyCredentials(username,password):
    if not UserExists(username):
        return gendict(301,"Invalid username"),True
        ## it send the message as the response
        ## and also the error=True
    if not verify_pw(username,password):
        return gendict(302,"Invalid password"),True
    
    ## if there is no error
    return None,False
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



class Classify(Resource):
    def post(self):
        ## get all the data
        ## with the image url
        postedData = request.get_json()
        username = postedData['username']
        password = postedData['password']
        url = postedData['url']

        response,error = verifyCredentials(username,password)
        if error:
            return jsonify(response)
        ## otherwise
        ## find the user token
        ## find the first user and then its token
        tokens = users.find({
            "username":username
        })[0]['Tokens']
        if tokens <=0:
            message = gendict(303,"Not Enough Token")
            return jsonify(message)
        ## get the images
        r = requests.get(url)
        ## get the total content in a variable
        response = {}
        ## open in the name of tmp.jpg
        ## and write the r.content in that file
        with open('temp.jpg','wb') as f: 
            f.write(r.content)
            ## we invoke our classify_image and get the result 
            ## with subprocess
            proc = subprocess.Popen("python classify_image.py --model_dir=. --image_file=temp.jpg",shell=True)
            ## let the process communicate with the program
            proc.communicate()[0]
            ## wait untill it finished
            proc.wait()
            ## and it will store the output with a json format in a file name text.txt
            ## and then you need to load it
            ## but to do that you need 
            with open('text.txt') as g:
                response = json.load(g) 
                ## we get the result
                ## he use the service so take his one token
                ## update the user table
        users.update({
            "username":username
        },{
            "$set":{
                "Tokens":tokens-1
            }
        })
        return response




## now the administrator can change any user token number
## add or remove
class Refill(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData['username']
        password = postedData['password']

        ## the ammount you want to refill
        ammount = postedData['ammount']
        if not UserExists(username):
            return jsonify(gendict(301,"invalid Username"))
        correct_pw = "123456789"
        if not password == correct_pw:
            return jsonify(gendict(304,"Invalid admin password"))
        ##if everything is ok

        users.update({
            "username":username
        },{
            "$set":{
                "Tokens":ammount
            }
        })
        return jsonify(gendict(200,"Refilled"))



## this is for testing purpose
class GetAllTheUsers(Resource):
    def get(self):
        all_users = list(users.find({}))
        return jsonify(json.dumps(all_users,default=str))


api.add_resource(Register,'/register')
api.add_resource(GetAllTheUsers,'/get_all_users')
api.add_resource(Classify,'/classify')
api.add_resource(Refill,'/refill')
if __name__ == '__main__':
    app.run(debug=True)