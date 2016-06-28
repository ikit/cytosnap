import os


DEBUG                     = True
SECRET_KEY                ="toto"
SESSION_TYPE			  ="mongodb"
DATABASE                  ="Cytosnap"
VERSION                   ="1.0"


BASEDIR                   = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER             = os.path.join(BASEDIR, 'images/')
UPLOAD_ALLOWED_EXTENSIONS = set(["png","jpg","jpeg","gif"])
STATIC_FOLDER			  = os.path.join(BASEDIR, 'templates/assets/')

