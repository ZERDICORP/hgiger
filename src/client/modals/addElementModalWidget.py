from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.modals.modalWidget import ModalWidget

class AddElementModalWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(AddElementModalWidget, self).__init__(parent, ui)

		self.setStyleSheet("".join([
			styles.lineEdit,
			styles.menuButton,
			styles.validator
		]))

		self.title = self.ui.createLabel(fontSize=14, alignment=Qt.AlignCenter)
		self.lineEdit = self.ui.createLineEdit(placeholder="Enter name..", alignment=Qt.AlignCenter, fontSize=12,
			returnAction=self.readyToAction, inputAction=self.updateErrorLine)
		self.errorLine = self.ui.createLabel(objectName="errorLine", fontSize=8, alignment=Qt.AlignCenter)

		self.mainLayout.addLayout(self.ui.createVLayout([
			self.title, 
			self.lineEdit, 
			self.errorLine
		]))
		self.setYesNoButtons(yesAction=self.readyToAction)

		self.parent.setChild(self)

	def readyToAction(self):
		self.updateErrorLine()
		if not self.isError:
			self.action(self.lineEdit.text())
			self.toggle()

	def updateErrorLine(self):
		if self.isOpen:
			error = self.ui.validator.validate(self.validateData["type"],
				value=self.lineEdit.text())
			self.errorLine.setText(error if error else "")
			self.isError = bool(error)
			self.ok.setDisabled(self.isError)
			self.updateTitle()

	def updateTitle(self):
		self.title.setText(f"{self.currentSection} > {self.ui.truncate(self.lineEdit.text(), 30)}")

	def clearErrorLine(self):
		self.isError = False
		self.errorLine.setText("")
		self.ok.setDisabled(False)

	def clearLineEdit(self):
		self.lineEdit.clear()
		self.lineEdit.clearFocus()

	def willBeOpen(self, validateData=None, currentSection=None, action=None):
		self.validateData = validateData
		self.currentSection = currentSection
		self.action = action
		self.lineEdit.setFocus()
		self.updateTitle()

	def willBeClosed(self):
		self.clearLineEdit()
		self.clearErrorLine()