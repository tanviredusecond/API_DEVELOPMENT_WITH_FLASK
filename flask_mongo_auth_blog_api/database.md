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
## also do it when you injecting data from the shell



comment the first import and uncomment the second 
when migrating
then comment it and un comment the first to run flask




first create the config file and add a class with config propertythen import the class and then add the configuratiom
to the app
create the app
create the db object
create a models.py and import the db in the models.py add the schema
import the schema class in the app.py
add a user

>>> u = User(username='susan', email='susan@example.com')
>>> db.session.add(u)
>>> db.session.commit()

>>> users = User.query.all()
>>> users
[<User john>, <User susan>]
>>> for u in users:
...     print(u.id, u.username)
...
1 john
2 susan



>>> u = User.query.get(1)
>>> u
<User john>



>>> u = User.query.get(1)
>>> p = Post(body='my first post!', author=u)
>>> db.session.add(p)
>>> db.session.commit()




