class AuthException(Exception):

	def __init__(self,username,user=None):
		self.username = username

class InvalidUsername(AuthException):
	pass

class InvalidPassword(AuthException):
	pass

class UserNotLoggedIn(AuthException):
	pass

class EmptyField(AuthException):
	pass

class EmailException(Exception):

	def __init__(self,email):
		self.email = email

class InvalidEmail(EmailException):
	pass
	