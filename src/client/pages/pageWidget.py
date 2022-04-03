from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject

class PageWidget(QWidget):
	def __init__(self, ui):
		super(PageWidget, self).__init__()
		self.ui = ui

	def afterInit(self):
		pass

	def settingByHistory(self):
		pass

	def getHistory(self):
		return self.ui.history.getHistory(self)