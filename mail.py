import smtplib
import requests
import ex

class _EmailVerifier(object):
	''' Email verifier that will be user as module level variable, the email verifier has only 1 method
	'''

	def __init__(self):
		self.api_pub_key = 'pubkey-cd34b35ce9a0f82dbd39e7377c59e4ea'
		self.mailgun_address = "https://api.mailgun.net/v2/address/validate"

	def verify_email(self,mail):
		'''takes a mail string and returns True or False depending wheather or not the mail exists'''
		response = requests.get(self.mailgun_address,auth=('api',self.api_pub_key),params = {'address':mail}).json()
		return response['is_valid']

class Email(object):

	'''Email object to send emails using gmail accounts

	'''

	def __init__(self,username):
		self.username = username
		self.domain = self.username.split('@')[-1]

	def send_email(self,data_to_send):
		if mail_verifier.verify_email(data_to_send['to']):
			try:
				server = smtplib.SMTP('smtp.'+self.domain,587)
				server.ehlo()
				server.starttls()
				server.ehlo()
				server.login(self.username,data_to_send['password'])
				message = 'To:' + data_to_send['to'] + '\n'+\
						'From:'+self.username+'\n'+\
						'Subject:'+ data_to_send['subject']+'\n'+\
						data_to_send['message']+'\n'
				server.sendmail(self.username,data_to_send['to'],message)
				server.close()
			except smtplib.SMTPAuthenticationError:
				raise ex.InvalidPassword(data_to_send['username'])
		else:
			raise ex.InvalidEmail(data_to_send['to'])


mail_verifier = _EmailVerifier()




if __name__=='__main__':
	p = mail_verifier
	p.verify_email('Suburb4nFilth@gmail.com')