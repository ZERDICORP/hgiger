from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.modals.modalWidget import ModalWidget

class TagsModalWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(TagsModalWidget, self).__init__(parent, ui)

		self.setStyleSheet("".join([
			styles.lineEdit,
			styles.menuButton,
			styles.validator
		]))

		self.lineEdit = self.ui.createLineEdit(placeholder="Enter text..", alignment=Qt.AlignCenter, fontSize=12,
			returnAction=self.readyToAction, inputAction=self.updateErrorLine)
		self.errorLine = self.ui.createLabel(objectName="errorLine", fontSize=8, alignment=Qt.AlignCenter)

		self.mainLayout.addLayout(self.ui.createVLayout([self.lineEdit, self.errorLine]))
		self.setYesNoButtons(yesAction=self.readyToAction)

		self.parent.setChild(self)

	def readyToAction(self):
		self.updateErrorLine()
		if not self.isError:
			self.action(self.tags)
			self.toggle()

	def updateErrorLine(self):
		if self.isOpen:
			self.tags = [tag.split(" ")[0] for tag in self.lineEdit.text().split("#") if tag not in ["", " "]]
			self.isError = "#" + " #".join(self.tags) == self.value
			self.errorLine.setText("value has not changed" if self.isError else "")
			self.ok.setDisabled(self.isError)

	def updateLineEdit(self):
		self.lineEdit.setText(self.value)
		self.lineEdit.selectAll()
		self.lineEdit.setFocus()

	def willBeOpen(self, value="", action=None):
		self.value = value
		self.action = action
		self.updateLineEdit()

	def clearErrorLine(self):
		self.isError = False
		self.errorLine.setText("")
		self.ok.setDisabled(self.isError)

	def clearLineEdit(self):
		self.lineEdit.clear()
		self.lineEdit.clearFocus()

	def willBeClosed(self):
		self.clearLineEdit()
		self.clearErrorLine()