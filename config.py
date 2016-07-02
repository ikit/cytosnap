import os

# Website config
DEBUG                     = True
SECRET_KEY                ="toto"
SESSION_TYPE			  ="mongodb"
VERSION                   ="1.0"

# Mongoengine database parameters
DATABASE                  ="Cytosnap"
SERVER 					  = "localhost"
PORT      				  = 27017

# Folders
BASEDIR                   = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER             = os.path.join(BASEDIR, 'images/')
UPLOAD_ALLOWED_EXTENSIONS = set(["png","jpg","jpeg","gif"])
STATIC_FOLDER			  = os.path.join(BASEDIR, 'templates/assets/')

