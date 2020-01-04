from flask import Flask,request,jsonify

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from config import Config
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy.orm import lazyload
app = Flask(__name__)

## importing configuratopn from the object
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
## fro migration we add the migrate
migrate = Migrate(app,db)
## api will set a abstraction of the app

## you must import the schema inthe main app

########################################
### take the db
############################
from models import Post,User
## modles goes here


## create the marshmello schema

class PostSchema(ma.Schema):
    class Meta:
        fields = ("body","timestamp","username")


post_schema = PostSchema()
## for single post

posts_schema = PostSchema(many=True)
## for many post


## create the post resources 
class PostsListResources(Resource):

    def get(self):
        ## egar loading
        posts = Post.query.join(User,Post.user_id==User.id).add_columns(User.username,User.email,Post.body,Post.timestamp).all()
        return posts_schema.dump(posts)

    
        
class PostListResources(Resource):
    def get(self,post_id):
        ## egar loading with the post_id
        posts = Post.query.join(User,Post.user_id==User.id).add_columns(User.username,User.email,Post.body,Post.timestamp).filter(Post.id==post_id)
        return posts_schema.dump(posts)

    def post(self):
       ## tou have to enter i two different database
       ## first take every thing from the necesary 
       ## its good if you have the mongodb




api.add_resource(PostsListResources,'/posts')
api.add_resource(PostListResources,'/posts/<int:post_id>')
if __name__ == '__main__':
    app.run(debug=True)


