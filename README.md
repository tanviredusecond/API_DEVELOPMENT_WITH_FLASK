# API_DEVELOPMENT_WITH_FLASK
API_DEVELOPMENT_WITH_FLASK

thse two line have to be added in the classify_image.py 
insted of just importin ternsorflow


import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()



command is 

pytohn3 classify_image.py --image_file <file_name>