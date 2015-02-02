import note
import Tkinter as tk
import tkMessageBox as mb
import tkFileDialog as fd
import ttk as ttk
import logging
import auth
import ex
import sys


class GUI(tk.Frame):
	
	def __init__(self,user_database,parent=None,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)

		''' make the window not resizable'''
		self.master.minsize(width = 400, height=250)
		self.master.maxsize(width=400, height = 250)
		self.pack()

		self.end = 'end-1c'

		self.login_frame = tk.Frame(self)
		self.register_frame = tk.Frame(self)
		self.in_frame = tk.Frame(self)
		self.profile_frame = tk.Frame(self.in_frame)

		self.auth = auth.Authenticate(user_database)

		self.noteVars = {}

		''' create the Notebook object, the current bucket to display, 
		variable containing a note's id and a dictionary of IntVar objects so we can check which button is selected'''
		self.current = 0
		self.current_selected = None

		'''login variables'''
		self.login_username = tk.StringVar()
		self.login_password = tk.StringVar()

		'''register variables'''
		self.registerVars = dict([('username',tk.StringVar()),
									('password',tk.StringVar()),
									('first',tk.StringVar()),
									('last',tk.StringVar()),
									('street',tk.StringVar()),
									('city',tk.StringVar()),
									('country',tk.StringVar()),
									('zip',tk.IntVar()),
									('email',tk.StringVar())])

		self.login()		

		#
		self.update_row = 2

	'''FUNC'''

	def clearWidget(self,to_clear,to_pack):
		to_clear.pack_forget()
		for child in to_clear.winfo_children():
			child.destroy()
		to_pack()

	def quit_program(self):
		self.auth.stop_database()
		self.quit()

	def clear_vars(self,var_dict):
		for key in var_dict:
			if key == 'zip':
				var_dict[key].set(0)
			else:
				var_dict[key].set('')

	def insert_text(self,insert_where,insert_what):
		insert_where.delete('1.0','end')
		insert_where.insert('1.0',insert_what)

	''' LOGIN / REGISTER '''

	def check_register_fields(self):
		if self.registerVars['password'].get() == '':
			raise ex.InvalidPassword(self.registerVars['username'])

	def save_credentials(self):
		try:
			self.check_register_fields()
			info_dict = dict([(key,value.get()) for key,value in self.registerVars.items()])
			self.auth.register(info_dict)
			self.clear_vars(self.registerVars)
			self.clearWidget(self.register_frame,self.login)
		except ex.InvalidUsername:
			mb.showwarning('Username Exists', 'The username already exists')
		except ex.InvalidPassword:
			mb.showwarning('InvalidPassword','Please choose another password')

	def register(self):
		self.register_frame.pack()
		self.clear_vars(self.registerVars)
		options = ('Username','Password','First Name','Last Name','Street','City','Country','Zip Code','Email Address','EmailPassword')
		row = 0
		for i in xrange(0,len(options),2):
			var = options[i].split()[0].lower()
			tk.Label(self.register_frame,text = options[i]).grid(row=row,column=0)
			tk.Entry(self.register_frame,textvariable=self.registerVars[var],width=15).grid(row=row,column=1)
			if i < 8:
				var2 = options[i+1].split()[0].lower()
				if options[i+1]=='Password':
					tk.Label(self.register_frame,text = 'Password').grid(row=row,column=2)
					tk.Entry(self.register_frame,textvariable=self.registerVars[var2],show='*',width=15).grid(row=row,column=3)
				else:
					tk.Label(self.register_frame,text = options[i+1]).grid(row=row,column=2)
					tk.Entry(self.register_frame,textvariable=self.registerVars[var2],width=15).grid(row=row,column=3)
			else:
				var2 = None
				row-=1
			row+=1
			
		tk.Button(self.register_frame,text='Cancel',command = lambda : self.clearWidget(self.register_frame,self.login)).grid(row=row,column=2)
		tk.Button(self.register_frame,text='Save',command = self.save_credentials).grid(row=row,column=3)

	def login(self):
		self.login_frame.pack()
		self.login_username.set('')
		self.login_password.set('')
		tk.Label(self.login_frame,text = 'Username').grid(row=0,column=0)
		tk.Entry(self.login_frame,textvariable = self.login_username).grid(row=0,column= 1,columnspan=2)
		tk.Label(self.login_frame,text = 'Password').grid(row=1,column=0)
		tk.Entry(self.login_frame,textvariable = self.login_password,show='*').grid(row=1,column = 1, columnspan=2)
		tk.Button(self.login_frame,text='Register',command = lambda : self.clearWidget(self.login_frame,self.register)).grid(row=2,column=1)
		tk.Button(self.login_frame,text='Login',command = self.check_credentials).grid(row=2,column=2)
		tk.Button(self.login_frame,text='Quit',command = self.quit_program).grid(row=2,column=0)

	def check_credentials(self):
		username = self.login_username.get()
		password = self.login_password.get()
		try:
			user = self.auth.login(username,password)
			if user:
				self.note = note.Notebook(username)
				self.clearWidget(self.login_frame,self.launch_notebook)
		except ex.InvalidPassword:
			mb.showwarning('Invalid Password','Invalid password')
		except ex.InvalidUsername:
			mb.showwarning('Invalid Username','Invalid username')

	def logout(self):
		self.auth.logout(self.login_username.get())
		self.clearWidget(self.in_frame,self.login)
		self.note.stop_database()


	''' AFTER LOGIN '''

	def launch_notebook(self):
		self.in_frame.pack()
		'''the frame for the buttons, the names of the notes and the actual note fields '''
		self.button_frame = tk.Frame(self.in_frame,bd=1,relief='sunken')
		self.button_frame.pack(side='top')
		self.sumary_frame = tk.Frame(self.in_frame,bd=1,relief='sunken')
		self.sumary_frame.pack(side='left',anchor='n')
		self.notes_frame = tk.Frame(self.in_frame)
		self.notes_frame.pack()

		#buttons
		tk.Button(self.button_frame,text='Save',command= self.save_note).grid(row=0,column=0)
		tk.Button(self.button_frame,text='Delete Note',command = self.delete_note).grid(row=0,column=1)
		tk.Button(self.button_frame,text='Logout',command = self.logout).grid(row=0,column=2)

		self.name = tk.Text(self.notes_frame,width=30,height=1,bd=1,selectborderwidth=0,relief='sunken')
		self.name.pack(anchor='w')
		self.tags = tk.Text(self.notes_frame,width=30,height=1,bd=1,selectborderwidth=0,relief='sunken')
		self.tags.pack(anchor='w')
		self.content = tk.Text(self.notes_frame,width=30,height=10,bd=1,selectborderwidth=0,relief='sunken')
		self.content.pack(anchor='w')

		self.updateSumary(0)


	def updateSumary(self,key):
		'''	
		updates the sumary frame

		'''
		for child in self.sumary_frame.winfo_children():
			child.destroy()
		tk.Button(self.sumary_frame,text='<',width=5,command=self.go_left).grid(row=0,column=0)
		tk.Button(self.sumary_frame,text='>',width=5,command=self.go_right).grid(row=0,column=1)
		notes = self.note.getNotes(key)
		if notes:
			for no in notes:
				note = self.note.getSingleNote(key,no)
				self.noteVars[note.id_number] = tk.IntVar()

				button = tk.Checkbutton(self.sumary_frame,text=note.name[:10],variable = self.noteVars[note.id_number],command = lambda note = note: self.display_note(note))
				button.trace = note.id_number
				button.grid(row=self.update_row,columnspan=2,sticky='w')
				self.update_row+=1
		self.current = key

	def display_note(self,note):
		''' displays the content of the note and deselects if there is more than one button selected '''
		for child in self.sumary_frame.children.values():
			try:
				if child.trace == note.id_number:
					pass
				else:
					child.deselect()
			except AttributeError:
				pass
		self.current_selected = note.id_number
		self.insert_text(self.name,note.name)
		self.insert_text(self.tags,''.join(note.tags))
		self.insert_text(self.content,note.content)

	def save_note(self):
		''' we create a dictionary with the info from the text vars and then decide to create a new note by checking if there is one selected
		or to edit existing one'''
		infoDict = dict([('name',self.name.get('1.0',self.end)),('tags',self.tags.get('1.0',self.end)),('content',self.content.get('1.0',self.end))])
		if any([self.noteVars[value].get() for value in self.noteVars.keys()]):
			self.note.edit_note(self.current,self.current_selected,infoDict)
		else:
			if self.name.get('1.0',self.end) != '':
				self.note.add_note(infoDict)
		self.insert_text(self.name,'')
		self.insert_text(self.tags,'')
		self.insert_text(self.content,'')
		self.updateSumary(0)

	def delete_note(self):
		temp = None
		for value in self.noteVars:
			if self.noteVars[value].get() == 1:
				self.note.delete_note(self.current,value)
				temp = value
		del self.noteVars[temp]
		self.insert_text(self.name,'')
		self.insert_text(self.tags,'')
		self.insert_text(self.content,'')
		self.updateSumary(self.current)

	def go_left(self):
		try:
			self.updateSumary(self.current-1)
		except KeyError:
			self.updateSumary(self.current)

	def go_right(self):
		try:
			self.updateSumary(self.current+1)
		except KeyError:
			self.updateSumary(self.current)