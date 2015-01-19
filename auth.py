import hashlib
import shelve
import ex
import datetime

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

	def __init__(self,databse_filename):

		self.filename = databse_filename
		self.start_database()

	def start_database(self):
		database_users = shelve.open(self.filename)
		if database_users:
			self.users = database_users['users']
		else:
			self.users = {}
		database_users.close()

	def stop_database(self):
		database_users = shelve.open(self.filename)
		database_users['users'] = self.users
		database_users.close()

	def register(self,info_dict):
		try:
			user = self.users[info_dict['username']]
			raise ex.InvalidUsername(info_dict['username'])
		except KeyError:
			user = User(info_dict)
			self.users[user.username] = user

	def login(self,username,password):
		try:
			if self.users[username].compare_passwords(password):
				self.users[username].login_status = True
			else:
				raise ex.InvalidPassword(username)
		except KeyError:
			raise ex.InvalidUsername(username)
		return True

	def logout(self,username):
		self.users[username].login_status=False
		return True	


if __name__=='__main__':
	test_user = {'username':'Dsa','password':'dsadsa','first':'Martin','last':'Spasov','street':'Baq','city':'Ganio','country':'Bulgaria','zip':'123','email':'akaka@gmail.com'}
	test_user_object = User(test_user)
	print test_user_object.get_info()
	print test_user_object.compare_passwords('asd')
	print test_user_object.password
	authenticate_object = Authenticate('user_log')
	authenticate_object.register(test_user)
	print authenticate_object.login(test_user['username'],test_user['password'])
	print authenticate_object.logout(test_user['username'])