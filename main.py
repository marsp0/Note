import datetime
import shelve
import logging
import os



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

	id_note = 0

	def __init__(self,filename):

		'''
		Object representing the entire notebook containing the individual notes
		PARAMS>
			;filename; - string - where the shelve is going to save the notes
			;notes; - dictionary - the individual note objects

		METHODS>
			;startDatabase; - None
			;stopDatabase; - None
		'''

		self.filename = filename
		self.path = 'database'

		self.start_database()


	def start_database(self):
		''' 
		Opens a shelve object checks to see if already exists and loads the info from it,
		if not creates an empty dictionary. Loads also a dictionary containing empty indexes
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
		else:
			self.notes = {}
			self.indexes_to_fill = {}
		database.close()

	def stop_database(self):
		''' 
		Opens a shelve object, saves the notes and closes the shelve object
		'''
		database = shelve.open(os.path.join(self.path,self.filename))
		database['notes'] = self.notes
		database['indexes_to_fill'] = self.indexes_to_fill
		database.close()

	def get_free_index(self):
		''' 
		function that returns tuple containing the first the bucket and an index
		'''
		indexes = sorted(self.indexes_to_fill.keys())
		if indexes:
			bucket = indexes[0]
			if len(self.indexes_to_fill[bucket]) > 1:
				index = self.indexes_to_fill[bucket][0]
				del self.indexes_to_fill[bucket][0]
				return bucket, index
			else:
				index = self.indexes_to_fill[bucket][0]
				del self.indexes_to_fill[bucket][0]
				return bucket,index

	def where_to_save(self):
		''' returns true if the there is free bucket in which we can save a note 
		(usually the last one since we dont create a new one if there is space in the previous)
		'''
		for key in self.notes:
			if len(self.notes[key]) < 7:
				return True
		return False

	def add_note(self,infoDict):
		''' 
		Adds a new note to the dictionary and increases the class variable self.id_note
		PARAMS>
			;infoDict; - dict - dict created in the gui part from the textvariables 
		'''
		if not self.indexes_to_fill:
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

	def delete_note(self,bucket,key):
		'''
		deletes a note from the notes dict and appends the index to the list containing indexes that need to be created
		PARAMS>
			;key; - int
		'''
		try:
			self.indexes_to_fill[bucket].append(key)
			
		except KeyError:
			self.indexes_to_fill[bucket] = [key]
		finally:
			del self.notes[bucket][key]

	def getNotes(self,current):
		''' 
		returns a bucket of 7 (less if its the last) of note objects
		'''
		if self.notes:
			list_to_return = self.notes[current]
			return list_to_return
		else:
			pass

	def getSingleNote(self,bucket,key):
		'''
		returns a single Note when given a bucket and a key
		'''
		return self.notes[bucket][key]


if __name__=='__main__':
	note = Note('Fuck','That bitch right in the pussay',['caramel','shoko'])
	print note.search('shoko')
	print note.search('bitch')
	print note.search('Crack')