import main
import Tkinter as tk
import tkMessageBox as mb
import tkFileDialog as fd
import ttk as ttk
import bwidget as bw
import threading

class GUI(tk.Frame):
	
	def __init__(self,filename,parent=None,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)

		''' make the window not resizable'''
		self.master.minsize(width = 400, height=250)
		self.master.maxsize(width=400, height = 250)
		self.pack()

		self.end = 'end-1c'


		''' create the Notebook object, the current bucket to display, 
		variable containing a note's id and a dictionary of IntVar objects so we can check which button is selected'''
		self.note = main.Notebook(filename)
		self.current = 0
		self.current_selected = None
		self.noteVars = {}

		'''the frame for the buttons, the names of the notes and the actual note fields '''
		self.button_frame = tk.Frame(self,bd=1,relief='sunken')
		self.button_frame.pack(side='top')
		self.sumary_frame = tk.Frame(self,bd=1,relief='sunken')
		self.sumary_frame.pack(side='left',anchor='n')
		self.notes_frame = tk.Frame(self)
		self.notes_frame.pack()

		#buttons
		tk.Button(self.button_frame,text='Save',command= self.save_note).grid(row=0,column=0)
		tk.Button(self.button_frame,text='Delete Note',command = self.delete_note).grid(row=0,column=1)
		tk.Button(self.button_frame,text='Quit',command = self.quit_program).grid(row=0,column=2)

		#
		self.update_row = 2	
		self.updateSumary(0)

		self.name = tk.Text(self.notes_frame,width=30,height=1,bd=1,selectborderwidth=0,relief='sunken')
		self.name.pack(anchor='w')
		self.tags = tk.Text(self.notes_frame,width=30,height=1,bd=1,selectborderwidth=0,relief='sunken')
		self.tags.pack(anchor='w')
		self.content = tk.Text(self.notes_frame,width=30,height=10,bd=1,selectborderwidth=0,relief='sunken')
		self.content.pack(anchor='w')

	def quit_program(self):
		self.note.stop_database()
		self.quit()


	def updateSumary(self,key):
		'''	
		updates the sumary frame

		'''
		for child in self.sumary_frame.winfo_children():
			child.destroy()
		tk.Button(self.sumary_frame,text='<',width=5,command=self.go_left).grid(row=0,column=0)
		tk.Button(self.sumary_frame,text='>',width=5,command=self.go_right).grid(row=0,column=1)
		notes = self.note.getNotes(key)
		print notes
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
			

	def insert_text(self,insert_where,insert_what):
		insert_where.delete('1.0','end')
		insert_where.insert('1.0',insert_what)

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
		for value in self.noteVars:
			if self.noteVars[value].get() == 1:
				self.note.delete_note(self.current,value)
		self.insert_text(self.name,'')
		self.insert_text(self.tags,'')
		self.insert_text(self.content,'')
		self.updateSumary(self.current)

	def go_left(self):
		self.updateSumary(self.current-1)

	def go_right(self):
		self.updateSumary(self.current+1)


if __name__=='__main__':
	p = GUI('database')
	p.mainloop()