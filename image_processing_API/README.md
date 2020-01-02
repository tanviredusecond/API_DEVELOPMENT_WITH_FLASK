# API_DEVELOPMENT_WITH_FLASK
API_DEVELOPMENT_WITH_FLASK

thse two line have to be added in the classify_image.py 
insted of just importin ternsorflow


import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

pip3 install -r requirment.txt
=>python app.py

=>two end point
  1) /register {"username":<>
                 "password":<>}
  
  2) /classify
    {"username":<>,
     "password":<>,
     "url":<public image url>}
