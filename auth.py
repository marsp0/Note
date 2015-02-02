import hashlib
import shelve
import ex
import datetime
from log import logging_decorator
import logging

class User(object):

	def __init__(self,info_dict):
		self.username = info_dict['username']
		self.password = self.make_password(info_dict['password'])
		self.first = info_dict['first']
		self.last = info_dict['last']
		self.street = info_dict['street']
		self.city = info_dict['city']
		self.country = info_dict['country']
		self.zip = info_dict['zip']
		self.email = info_dict['email']
		self.login_status = False

	def get_info(self):
		info_dict = dict([('username',self.username),
							('first',self.first),
							('last',self.last),
							('street',self.street),
							('city',self.city),
							('country',self.country),
							('zip',self.zip),
							('email',self.email)])
		return info_dict

	def make_password(self,password):
		digested = hashlib.md5()
		digested.update(password)
		return digested.digest()

	def compare_passwords(self,password):
		given_password = hashlib.md5()
		given_password.update(password)
		return self.password == given_password.digest()


class Authenticate(object):

	logger =logging.getLogger('Users')
	logger.setLevel(logging.DEBUG)
	handler = logging.FileHandler('auth_log.log')
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	def __init__(self,databse_filename):

		self.filename = databse_filename
		self.start_database()


	@logging_decorator(logger,'Starting User Database')
	def start_database(self):
		database_users = shelve.open(self.filename)
		if database_users:
			self.users = database_users['users']
		else:
			self.users = {}
		database_users.close()

	@logging_decorator(logger,'Stopping User Database')
	def stop_database(self):
		database_users = shelve.open(self.filename)
		database_users['users'] = self.users
		database_users.close()

	@logging_decorator(logger, 'Registering a new user')
	def register(self,info_dict):
		try:
			user = self.users[info_dict['username']]
			raise ex.InvalidUsername(info_dict['username'])
		except KeyError:
			user = User(info_dict)
			self.users[user.username] = user

	@logging_decorator(logger, 'Loging in')
	def login(self,username,password):
		try:
			if self.users[username].compare_passwords(password):
				self.users[username].login_status = True
			else:
				raise ex.InvalidPassword(username)
		except KeyError:
			raise ex.InvalidUsername(username)
		return True

	@logging_decorator(logger, 'Loging out')
	def logout(self,username):
		self.users[username].login_status=False
		return True	