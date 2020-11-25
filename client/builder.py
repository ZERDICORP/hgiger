from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from client.ui import UI
from client.tools.history import History
from client.pages.cellsPage import CellsPage
from client.pages.hintsPage import HintsPage
from client.pages.hintPage import HintPage

class Builder(UI):
	def __init__(self, manager):
		super(Builder, self).__init__()
		self.manager = manager
		self.history = History()
		# (↓) [-open start page-]
		self.openPage(pageCreator=self.createCellsPage)

	def rebuild(self):
		self.openPage(self.pageCreator)

	def openPage(self, pageCreator):
		self.pageCreator = pageCreator
		self.setCentralWidget(self.pageCreator())
		self.centralWidget().settingByHistory()
		self.centralWidget().afterInit()
		self.setModals()

	def createCellsPage(self):
		return CellsPage(self, self.manager.cellSections, self.manager.cells)

	def createHintsPage(self, cellId):
		self.manager.openCell(cellId)
		return HintsPage(self, self.manager.hintSections, self.manager.hints)

	def createHintPage(self, hintId):
		self.manager.openHint(hintId)
		return HintPage(self, self.manager.currentHint)