from PyQt5.QtCore import Qt
from client.tools.staticManager import styles
from client.modals.modalWidget import ModalWidget

class MoveCellModalWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(MoveCellModalWidget, self).__init__(parent, ui)

		self.setStyleSheet("".join([
			styles.comboBox,
			styles.menuButton,
			styles.validator
		]))

		self.sections = [section["name"] for section in self.ui.manager.cellSections]
		self.requestData = {}

		self.title = self.ui.createLabel(fontSize=16, alignment=Qt.AlignCenter)
		self.cbox = self.ui.createComboBox(activated=self.updateTitle)

		self.mainLayout.addLayout(self.ui.createVLayout([self.title, self.cbox]))
		self.setYesNoButtons(yesAction=self.readyToAction)

		self.parent.setChild(self)

	def readyToAction(self):
		newValue = self.cbox.currentText()
		if newValue:
			self.ui.manager.reception(self.ui.manager.requestType.MOVE_CELL,
				cellId=self.objectId,
				newValue=newValue)
			self.toggle()

	def updateTitle(self):
		self.title.setText(f"Move \"{self.objectName}\" to \"{self.cbox.currentText()}\"")

	def updateCbox(self):
		self.cbox.clear()
		self.cbox.addItems([item for item in self.sections if item != self.objectSection])		

	def willBeOpen(self, objectName, objectId, objectSection):
		self.objectName = objectName
		self.objectId = objectId
		self.objectSection = objectSection
		self.updateCbox()
		self.updateTitle()