#!env/python3
from flask import Flask
from flask import Flask, jsonify,render_template
from model import *

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('hello.html')

@app.route('/images/')
def get_images():
	return jsonify({"results":[i.to_obj() for i in Image.objects.all()]})


@app.route('/images/<image_id>')
def get_image(image_id):
	return jsonify({"results": Image.objects.get(pk=image_id).to_obj()})



if __name__ == '__main__':
	app.run(debug=True)