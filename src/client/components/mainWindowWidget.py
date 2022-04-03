from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize, QMetaObject

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		
		self.setObjectName("MainWindow")
		
		self.WSize = 800, 600
		
		self.resize(*self.WSize)
		self.setMinimumSize(QSize(*self.WSize))
		self.setMaximumSize(QSize(*self.WSize))

		QMetaObject.connectSlotsByName(self)