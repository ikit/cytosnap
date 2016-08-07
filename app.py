#!env/python3
import os
import random
import itertools
import uuid

from random import shuffle
from flask import Flask, jsonify, render_template, session, request
from flask.ext.session import Session
from flask.ext.login import LoginManager
from mongoengine import *
from bson.objectid import ObjectId

from model import *



''' initialization of application '''
app = Flask(__name__)

''' load configuration from config.py '''
app.config.from_pyfile("config.py")

''' creat/connect database '''
connect(app.config["DATABASE"])

''' Create upload directory if not exists '''
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
	os.makedirs(app.config["UPLOAD_FOLDER"])

''' Manage user session '''
Session(app)






''' API Tools '''
def success_response(data = None):
	if data is None:
		results = {"success":True}
	else:
		results = {"success":True, "data":data}
	return jsonify(results)


def error_response(message="Unknown", code="0"):
	results = {"success":False, "message":message, "error_code":code}
	return jsonify(results)


''' User authentication '''
def check_auth(f):
	def called(*args, **kargs):
		if 'user_id' in session:
			user = User.from_id(session["user_id"])
			if user is not None:
				return f(*args, **kargs)
		return error_response("Authentification is required", 403)
	return called

def current_user():
	if 'user_id' in session:
		user = User.from_id(session["user_id"])
		return user
	return None



''' check authent on all request '''
@app.before_request
def before_request():
	if session and "user_id" in session:
		print("Check auth : " + str(session))
		if 'user_id' in session:
			user = User.from_id(ObjectId(session["user_id"]))
			if user is not None:
				print ("Session Valid")
				session['username'] = user.fullname
				return

		print ("Session not valid")
		return error_response("Authentification is required", 403)
	else:
		if request.url_root == 'login_user' or request.url_root == 'login':
			print("Trying to connect, not checking session auth yet")
		else:
			print (request.url_root)
			print ("Session not valid -> need to login")
			#return error_response("Authentification is required", 403)

'''
	if request :
		print( "Endpoint : " + str(request))
	else:
		print("Endpoint : None")
    #if 'logged_in' not in session and request.endpoint != 'login':

'''

















@app.route('/')
def index():
	return render_template('welcom.html')


@app.route('/login/', methods=['GET'])
def login_page():
	return render_template('login.html')


@app.route('/stats/', methods=['GET'])
def stats_global():
	return render_template('welcom.html')

@app.route('/stats/<user_id>', methods=['GET'])
def stats_user():
	return render_template('welcom.html')








''' Model API '''




@app.route('/images/')
def get_images():
	return jsonify({"results":[i.export_data() for i in Image.objects.all()]})


@app.route('/images/<image_id>')
def get_image(image_id):
	return jsonify({"results": Image.objects.get(pk=image_id).export_data()})

@app.route('/images/', methods=['POST'])
def new_image():
	image = Image()
	image.import_data(request.json)
	Image.objects.add(image)
	Image.save()
	return jsonify({"results": image.export_data()})

@app.route('/images/<image_id>', methods=['PUT'])
def edit_image(image_id):
	image = Image.objects.get(pk=image_id)
	image.import_data(request.json)
	image.save()
	return {}

@app.route('/images/random', methods=['GET'])
def random_image():
	image = Image.objects.skip(random.randrange(0, Image.objects.count())).first()
	props = Image.objects.distinct("answer")
	uid = uuid.uuid4()
	shuffle(props)
	questions = props[0:6]
	if image.answer not in questions:
		questions[random.randrange(0,6)] = image.answer

	session[uid] = (user.id, image.answer)
	return jsonify({"results": dict(itertools.chain(image.export_data().items(), {"questions" : questions}.items(), {"qid" : uid})) })

@app.route('/images/answer', methods=['POST'])
def answer_image():
	data = request.get_json()
	uid = data.get('uid')
	answer = data.get('answer')
	user_answer = session.get(uid)

	if (answer == user_answer):
		# good !
		# save stat
		# continue with next question
		# finish
		pass
	else:
		# bad ...
		# next question




	return random_image()




@app.route('/users/')
def get_users():
	return jsonify({"results":[u.export_data() for u in User.objects.all()]})


@app.route('/users/<user_id>')
def get_user(user_id):
	return jsonify({"results": User.objects.get(pk=user_id).export_data()})

@app.route('/users/', methods=['POST'])
def new_user():
	user = User()
	user.import_data(request.json)
	user.objects.add(image)
	user.save()
	return jsonify({"results": user.export_data()})

@app.route('/users/<user_id>', methods=['PUT'])
def edit_user(user_id):
	image = Image.objects.get(pk=user_id)
	image.import_data(request.json)
	image.save()
	return {}



@app.route('/users/login', methods=['GET'])
def login_user():
	print ("LOGIN")
	data = request.get_json(force=False)
	login    = data.get("login")
	password = data.get("password")

	user = User.objects(login=login).first()

	if user is None:
		return error_response("Bad login or password")
	else:
		session['user_id'] = str(user.id)

	print("Login user ", login, " : ", session["user_id"])
	return success_response(session['user_id'])



@app.route('/users/logout')
def logout_user():
	print("Logout - delete session : ", session["user_id"])
	session.pop("user_id", None)
	return success_response()






if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")