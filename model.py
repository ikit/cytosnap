from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from bson.objectid import ObjectId

class Image(Document):
	path = StringField(required=True)
	answer = StringField(max_length=50)
	asked_count = IntField()
	good_count = IntField()


	def __str__(self):
		return self.path


	def export_data(self):
		return {
			"path":self.path, 
			"id": str(self.pk)
			}


	def import_data(self, data):
		try:
			self.path        = data['path']
			self.questions   = data['questions']
			self.answers     = data['answers']
			self.asked_count = data['asked_count']
			self.good_count  = data['good_count']
		except KeyError as e:
			raise ValidationError('Invalid order: missing ' + e.args[0])

		return self




class User(Document):
	fullname = StringField(max_length=255)
	login = StringField(max_length=50, required=True)
	password_hash = StringField(max_length=255, required=True)
	service = StringField(max_length=255)
	function = StringField(max_length=255)
	last_habilitation = Dae

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def generate_auth_token(self, expires_in=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
		return s.dumps({'id': self.id}).decode('utf-8')

	def export_data(self):
		return {
			"fullname":self.fullname, 
			"id": str(self.pk)
			}

	def import_data(self, data):
		try:
			self.fullname      = data['fullname']
			self.login         = data['login']
			set_password(data['password_hash'])
		except KeyError as e:
			raise ValidationError('Invalid order: missing ' + e.args[0])
		return self

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return None
		return User.objects.get(pk=data['id'])

	@staticmethod
	def from_id(user_id):
		if not ObjectId.is_valid(user_id):
			return None;
		
		user = User.objects.get(pk=user_id)
		return user
