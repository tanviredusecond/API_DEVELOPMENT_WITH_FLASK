from flask import Flask,request,jsonify

## adding the database module
from flask_sqlalchemy import SQLAlchemy

## this is for serialization 
from flask_marshmallow import Marshmallow

## adding the database configuration in the app
## and initialize the app
## using sqlite database

from flask_restful import Api,Resource

## now add the api with app


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # new
db = SQLAlchemy(app) # new add the databse functionality with the app
ma = Marshmallow(app)
## adding the Marshmello for the serialization
## this is for serialization
api = Api(app)



## this is the database class
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(255))


## making the marshmellow schema about how this data is going to show

class PostSchema(ma.Schema):
    ## meta field is used for the representation
    ## this is not going to change anything related to the object
    ## just parse the information and send specfic data
    
    class Meta:
        fields = ("id","title","content")
        ## this three files will be used


## we create this object now but for the meta class it will sending the json
## we create two different object
## one for the single post and 
## one for the multiple post
post_schema = PostSchema()
posts_schema = PostSchema(many=True)



## create the Api Schema

class PostListResources(Resource):
    ## this is the get request
    def get(self):
        ## get all the post
        posts = Post.query.all()
        #print(posts)
        return posts_schema.dump(posts)
        ## we dump it with the marshmello schema 
        ## so it will serializer
    def post(self):
        new_post = Post(
            title = request.json['title'],
            content = request.json['content']
        )
        db.session.add(new_post) ## adding 
        ## committting
        db.session.commit()
        ## return what you added
        ## this will be post schema insted of 
        ## posts schema
        #print (new_post)
        return post_schema.dump(new_post)

    ## adding patch option/put option





## create new resorces for fetching individual post
class PostResource(Resource):
    def get(self,post_id):
        ## get the post using the post ID
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)
    def patch(self,post_id):
        post = Post.query.get_or_404(post_id)

        ## checking if the title in the 
        ## json file and the content

        if 'title' in request.json:
            # change the title
            post.title = request.json['title']
        if 'content' in request.json:
            post.content = request.json['content']

        ## commit the post 
        db.session.commit()
        ## now return the edited post
        return post_schema.dump(post) 
    

    def delete(self,post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({
            "msg": "Successfully deleted"
        })

api.add_resource(PostResource,'/posts/<int:post_id>')
api.add_resource(PostListResources,'/posts')









if __name__ == '__main__':
    app.run(debug=True)