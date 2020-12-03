from PyQt5.QtCore import Qt
from client.tools.staticManager import styles
from client.modals.modalWidget import ModalWidget

class MoveHintModalWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(MoveHintModalWidget, self).__init__(parent, ui)

		self.setStyleSheet("".join([
			styles.comboBox,
			styles.menuButton,
			styles.validator
		]))

		self.requestData = {}
		self.hasBeenOpen = True

		self.title = self.ui.createLabel(fontSize=16, alignment=Qt.AlignCenter)
		self.cellSectionsCbox = self.ui.createComboBox(items=[section["name"] for section in self.ui.manager.cellSections], 
			activated=lambda index: self.updateCellSectionsCbox(index=index))
		self.cellsCbox = self.ui.createComboBox(items=[cell["name"] for cell in self.ui.manager.cells], 
			activated=lambda index: self.updateCellsCbox(index=index))
		self.hintSectionsCbox = self.ui.createComboBox(items=[section["name"] for section in self.ui.manager.hintSections], 
			activated=lambda index: self.updateHintSectionsCbox(index=index))

		self.mainLayout.addLayout(self.ui.createVLayout([
			self.title, 
			self.cellSectionsCbox, 
			self.cellsCbox,
			self.hintSectionsCbox
		]))
		self.setYesNoButtons(yesAction=self.readyToAction)

		self.parent.setChild(self)

	def haveAnyReasonToOpen(self, objectSection):
		self.objectSection = objectSection
		self.getSections()
		return not bool(self.sections)

	def readyToAction(self):
		newPath = self.getCurrentPath()
		newPath[1] = self.cells[self.cellsCbox.currentIndex()]["id"]
		self.ui.manager.reception(self.ui.manager.requestType.MOVE_HINT,
			hintId=self.objectId,
			newPath=newPath)
		self.toggle()

	def getCurrentPath(self):
		return [
			self.cellSectionsCbox.currentText(), 
			self.cellsCbox.currentText(), 
			self.hintSectionsCbox.currentText()
		]

	def updateTitle(self):
		path = " > ".join([f"\"{item}\"" for item in self.getCurrentPath()])
		self.title.setText(f"Move \"{self.ui.truncate(string=self.objectName, length=30)}\" to \n{path}")

	def cellHaveMoreSections(self, cell):
		return True if len(cell["body"][0]) > 1 else cell["body"][0][0]["name"] != self.objectSection

	def sectionHaveMoreCells(self, cells):
		return True if len(cells) > 1 else self.cellHaveMoreSections(cells[0])

	def getSections(self):
		self.sections = [section for section in self.ui.manager.cellSections if self.sectionHaveMoreCells(
			cells=[cell for cell in self.ui.manager.cells if cell["section"] == section["name"]])]

	def getCells(self, index):
		self.cells = [cell for cell in self.ui.manager.cells 
			if cell["section"] == self.sections[index]["name"] and self.cellHaveMoreSections(cell)]

	def updateCellSectionsCbox(self, index=0):
		self.getSections()
		self.cellSectionsCbox.clear()
		self.cellSectionsCbox.addItems([section["name"] for section in self.sections])
		self.cellSectionsCbox.setCurrentIndex(index)
		self.updateCellsCbox(cellSectionIndex=index)

	def updateCellsCbox(self, index=0, cellSectionIndex=None):
		cellSectionIndex = cellSectionIndex if cellSectionIndex != None else self.cellSectionsCbox.currentIndex()
		self.getCells(cellSectionIndex)
		if self.hasBeenOpen:
			cellIndex = [i for i, cell in enumerate(self.cells) if cell["id"] == self.ui.manager.currentCell["id"]]
			if cellIndex:
				index = cellIndex[0]
			self.hasBeenOpen = False
		self.cellsCbox.clear()
		self.cellsCbox.addItems([cell["name"] for cell in self.cells])
		self.cellsCbox.setCurrentIndex(index)
		self.updateHintSectionsCbox(cellIndex=self.ui.manager.cells.index(self.cells[index]))

	def updateHintSectionsCbox(self, index=0, cellIndex=None):
		if cellIndex != None:
			self.hintSectionsCbox.clear()
			self.hintSectionsCbox.addItems([section["name"] for section in self.ui.manager.cells[cellIndex]["body"][0] if section["name"] != self.objectSection])		
		self.hintSectionsCbox.setCurrentIndex(index)
		self.updateTitle()

	def willBeOpen(self, objectName, objectId, objectSection):
		self.objectName = objectName
		self.objectId = objectId
		self.objectSection = objectSection
		self.updateCellSectionsCbox(0)