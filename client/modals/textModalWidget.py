from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.modals.modalWidget import ModalWidget

class TextModalWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(TextModalWidget, self).__init__(parent, ui)

		self.setStyleSheet("".join([
			styles.menuButton,
			styles.validator,
			styles.textEdit
		]))

		self.textEdit = self.ui.createTextEdit(placeholder="Enter text..", objectName="borderBottom", inputAction=self.updateErrorLine)
		self.errorLine = self.ui.createLabel(objectName="errorLine", fontSize=8, alignment=Qt.AlignCenter)
		self.errorLine.setMaximumHeight(self.ui.getFontHeight(fontSize=8))

		self.mainLayout.addLayout(self.ui.createVLayout([self.textEdit, self.errorLine]))
		self.setYesNoButtons(yesAction=self.readyToAction)

		self.parent.setChild(self, alignment=None)

	def readyToAction(self):
		self.updateErrorLine()
		if not self.isError:
			self.action(self.textEdit.toPlainText())
			self.toggle()

	def updateErrorLine(self):
		if self.isOpen:
			error = self.ui.validator.validate(self.validateData["type"],
				value=self.textEdit.toPlainText(),
				source=None if not self.value else self.value)
			self.errorLine.setText(error if error else "")
			self.isError = bool(error)
			self.ok.setDisabled(self.isError)

	def updateTextEdit(self):
		self.textEdit.setPlainText(self.value)
		self.textEdit.setFocus()

	def willBeOpen(self, validateData=None, value="", action=None):
		self.validateData = validateData
		self.value = value
		self.action = action
		self.updateTextEdit()

	def clearErrorLine(self):
		self.isError = False
		self.errorLine.setText("")
		self.ok.setDisabled(self.isError)

	def clearTextEdit(self):
		self.textEdit.clear()
		self.textEdit.clearFocus()

	def willBeClosed(self):
		self.clearTextEdit()
		self.clearErrorLine()