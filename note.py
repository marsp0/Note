import datetime
import shelve
import logging
import os
from log import logging_decorator
import logging



class Note(object):	

	def __init__(self,idNumber,name,content,tags):
		''' 
		Note object representing single note
		PARAMS>
			;name; - string 
			;content; - string
			;date; - datetime object
			;tags; - list of strings
			;idNumber; - int

		METHODS>
			;search; - boolean - 

		'''
		self.id_number = idNumber   
		self.name = name
		self.content = content
		self.date = datetime.datetime.today()
		self.tags = tags

	def search(self,to_find):
		''' 
		Checks to see if to_find is in the tags or in the content 
		PARAMS>
			;to_find; - string
		'''

		return (to_find in self.tags) or (to_find in self.content) or (to_find in self.name)

class Notebook(object):

	logger = logging.getLogger('Notebook')
	logger.setLevel(logging.DEBUG)
	handler = logging.FileHandler('auth_log.log')
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	def __init__(self,filename):

		'''
		Object representing the entire notebook containing the individual notes
		PARAMS>
			;filename; - string - where the shelve is going to save the notes, the user's username is used for the name of the note database

		VARS>
			;logger; - the logger name
			;handler; - the file where the logs are written
			;formatter; - format of the logs
			;self.path; - string - the name of the folder in which are stored the different users note databases
			;self.notes; - the dictionary containing the users notes. The structure is in the form {bucket : {key : note} }
			;self.indexes_to_fill; - dictionary containing the indexes of the deleted notes {bucket : [indexes]}
			;self.id_note; - int - keeping track of the notes in the database and is used as key of the notes

		METHODS>
			;startDatabase; - None
			;stopDatabase; - None
		'''

		self.filename = filename
		self.path = 'database'

		self.start_database()

	@logging_decorator(logger,'Starting Database')
	def start_database(self):
		''' 
		Opens a shelve object and loads the notes,indexes to fill and the id variable
		 '''
		if os.path.isdir(self.path):
			path = os.path.join(self.path,self.filename)
		else:
			os.mkdir(self.path)
			path = os.path.join(self.path,self.filename)
		database = shelve.open(path)	
		if database:
			self.notes = database['notes']
			self.indexes_to_fill = database['indexes_to_fill']
			self.id_note = int(database['id_note'])
		else:
			self.notes = {}
			self.indexes_to_fill = {}
			self.id_note = 0
		database.close()

	@logging_decorator(logger, 'Stopping Database')
	def stop_database(self):
		''' 
		Opens a shelve object, saves the notes and closes the shelve object
		'''
		database = shelve.open(os.path.join(self.path,self.filename))
		database['notes'] = self.notes
		database['indexes_to_fill'] = self.indexes_to_fill
		database['id_note'] = self.id_note
		database.close()

	def get_free_index(self):
		''' 
		function that returns tuple containing the first bucket and an index available
		'''
		buckets = sorted(self.indexes_to_fill.keys())
		if buckets:
			single_bucket = buckets[0]

			if len(self.indexes_to_fill[single_bucket]) >= 1:
				index = self.indexes_to_fill[single_bucket][0]
				del self.indexes_to_fill[single_bucket][0]
				if len(self.indexes_to_fill[single_bucket]) == 0:
					del self.indexes_to_fill[single_bucket]
				return single_bucket, index
			else:
				return single_bucket,single_bucket*7

	def where_to_save(self):
		''' returns true if the there is free bucket in which we can save a note 
		(usually the last one since we dont create a new one if there is space in the previous)
		'''
		for key in self.notes:
			if len(self.notes[key]) < 7:
				return True
		return False

	@logging_decorator(logger, 'Adding Note')
	def add_note(self,infoDict):
		''' 
		Adds a new note to the dictionary and increases the class variable self.id_note
		PARAMS>
			;infoDict; - dict - dict created in the gui part from the textvariables 
		'''
		if len(self.indexes_to_fill) == 0:
			note = Note(self.id_note,infoDict['name'],infoDict['content'],infoDict['tags'].split())
			index_where = len(self.notes.keys())
			if self.where_to_save():
				self.notes[index_where-1][self.id_note] = note
			else:
				self.notes[index_where] = {}
				self.notes[index_where][self.id_note] = note
			self.id_note+=1
		else:
			bucket, index = self.get_free_index()
			note = Note(index,infoDict['name'],infoDict['content'],infoDict['tags'])
			self.notes[bucket][index] = note

	@logging_decorator(logger, 'Editing Note')
	def edit_note(self,bucket,key,infoDict):
		'''
		Edit a note from the dictionary
		PARAMS>
			;key; - int
			;infoDict; - dict - dict created in the gui part from the textvariables
		'''

		self.notes[bucket][key].name = infoDict['name']
		self.notes[bucket][key].content = infoDict['content']
		self.notes[bucket][key].tags = infoDict['tags']

	@logging_decorator(logger, 'Deleting Note')
	def delete_note(self,bucket,key):
		'''
		deletes a note from the notes dict and appends the index to the list containing indexes that need to be created
		PARAMS>
			;key; - int
			;bucket; - int
		'''
		try:
			#we append the index (1-7) to the bucket list with empty indexes to fill
			print self.indexes_to_fill
			self.indexes_to_fill[bucket].append(key)
		except KeyError:
			#if there is no such bucket key we create a list and add the index to the list
			self.indexes_to_fill[bucket] = [key]
		del self.notes[bucket][key]

	def getNotes(self,current):
		''' 
		returns a bucket of 7 (less if its the last) of note objects
		'''

		if self.notes:
			dict_to_return = self.notes[current]
			return dict_to_return
		else:
			pass

	def getSingleNote(self,bucket,key):
		'''
		returns a single Note when given a bucket and a key
		'''
		return self.notes[bucket][key]
