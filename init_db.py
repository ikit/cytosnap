#!env/python3
import os
import zipfile
import re

from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import *
from model import *


DATABASE      = "Cytosnap"
IMAGES_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "/static/images/"


''' creat/connect database '''
connect(DATABASE)





usr = User()
usr.fullname = "Escuret Antoine"
usr.login 	 = "aescuret"
password	 = "aescuret"
usr.password_hash = generate_password_hash(password)
usr.save()


zip_ref = zipfile.ZipFile('init_images.zip', 'r')
zip_ref.extractall(IMAGES_FOLDER)
zip_ref.close()


print ("Images extract into : " + IMAGES_FOLDER)

for file in os.listdir(IMAGES_FOLDER):
	if file.endswith(".JPG"):
		img = Image()
		img.asked_count = 0
		img.good_count  = 0

		# get the answer
		img.answer = os.path.splitext(file)[0]
		# remove digit if exists
		m = re.search("\d", img.answer)
		if m:
			img.answer = img.answer[0:m.start()]

		# get id and rename/move file
		img.path =  "tmp.jpg"
		img.save() # first save to get an id in database
		img.path = str(img.id) + ".jpg"
		os.rename(IMAGES_FOLDER + file, IMAGES_FOLDER + img.path)
		img.save() 
		print ("Process " + file + "\t -> " + img.path + " [" + img.answer + "]")