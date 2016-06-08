from mongoengine import *

connect('CytoSnap')


class Image(Document):
	path = StringField(required=True)
	questions = StringField(max_length=50)
	answer = StringField(max_length=50)

	def __str__(self):
		return self.path

	def to_obj(self):
		d = {"path":self.path, "id": str(self.pk) }
		return d 

