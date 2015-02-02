import note
import gui
import sys

class Main(object):

	def __init__(self,filename):
		self.gui = gui.GUI(filename)
		self.gui.mainloop()

if __name__=='__main__':
	p = Main(sys.argv[1])