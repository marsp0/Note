import unittest
from note import *
from auth import *


class TestNote(unittest.TestCase):

	def setUp(self):
		self.note = Note(0,'NoteName','Note content',['tag1','tag2'])

	def test_attributes(self):
		self.assertEqual(self.note.id_number,0)
		self.assertEqual(self.note.name ,'NoteName')
		self.assertEqual(self.note.content ,'Note content')
		self.assertEqual(self.note.tags ,['tag1','tag2'])

	def test_search(self):
		self.assertEqual(self.note.search('tag1'),True)
		self.assertEqual(self.note.search('tag'),False)

	def tearDown(self):
		del self.note

class TestNotebook(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.notebook = Notebook('test_database')

		cls.info_dict = {'name':'NoteName','content':'Note content','tags':'tag1,tag2'}
		cls.id_note = 0

	def test_add(self):
		self.assertEqual(self.notebook.add_note(self.info_dict),None)

	def test_edit(self):
		self.info_dict['name'] = 'Name'
		self.assertEqual(self.notebook.edit_note(0,self.id_note,self.info_dict),None)

	def test_get_single(self):
		self.assertEqual(self.notebook.getSingleNote(0,0).name,'Name')

	def test_get_notes(self):
		self.assertEqual(len(self.notebook.getNotes(0)),1)

	@classmethod
	def tearDownClass(cls):
		del cls.notebook

class TesUser(unittest.TestCase):

	def setUp(self):
		self.user_info = {'username':'Dsa','password':'dsadsa','first':'Martin','last':'Spasov','street':'Baq','city':'Ganio','country':'Bulgaria','zip':'123','email':'akaka@gmail.com'}
		self.user = User(self.user_info)

	def test_get_info(self):
		self.assertEqual(len(self.user.get_info()), len(self.user_info.keys()[:-1]))

	def test_password(self):
		self.assertEqual(self.user.compare_passwords('dsadsa'),True)

class TestAuthenticate(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.auth = Authenticate('test_user')
		cls.user_info = {'username':'Dsa','password':'dsadsa','first':'Martin','last':'Spasov','street':'Baq','city':'Ganio','country':'Bulgaria','zip':'123','email':'akaka@gmail.com'}
		cls.auth.register(cls.user_info)

	#def test_register(self):
	#	self.assertEqual(self.auth.register(self.user_info),None)

	def test_login(self):	
		self.assertEqual(self.auth.login(self.user_info['username'],self.user_info['password']),True)

	def test_logout(self):
		self.assertEqual(self.auth.logout(self.user_info['username']),True)
if __name__=='__main__':
	unittest.main()