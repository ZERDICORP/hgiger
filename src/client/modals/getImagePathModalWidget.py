from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.modals.modalWidget import ModalWidget

class GetImagePathModalWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(GetImagePathModalWidget, self).__init__(parent, ui)
		
		self.setStyleSheet("".join([
			styles.lineEdit,
			styles.menuButton,
			styles.validator,
		]))
		
		self.iconSize = (30, 30)

		self.icon = self.ui.createPixmap(objectName="icon", fontSize=10)
		self.title = self.ui.createLabel(fontSize=12, objectName="size", alignment=Qt.AlignHCenter)
		self.lineEdit = self.ui.createLineEdit(placeholder="Enter path..", alignment=Qt.AlignCenter, fontSize=12,
			returnAction=self.readyToAction, inputAction=self.updateErrorLine)
		self.errorLine = self.ui.createLabel(objectName="errorLine", fontSize=8, alignment=Qt.AlignCenter)

		self.mainLayout.addStretch(1)
		self.mainLayout.addLayout(self.ui.createVLayout([
			self.title,
			self.ui.createVLayout([self.icon], alignment=Qt.AlignCenter),
			self.lineEdit, 
			self.errorLine
		]))
		
		self.openExplorerButton = self.ui.createPushButton(iconPath=assetsPath.folder, action=self.openExplorer, fixedSize=(30, 30), eventFilter=self)
		self.setYesNoButtons(yesAction=self.readyToAction, between=[self.openExplorerButton])

		self.parent.setChild(self)

	def readyToAction(self):
		self.updateErrorLine()
		if not self.isError:
			self.action(self.lineEdit.text())
			self.toggle()

	def openExplorer(self):
		path = self.ui.openExplorer()
		if path:
			self.lineEdit.setText(path)

	def updateErrorLine(self):
		if self.isOpen:
			error = self.ui.validator.validate(self.validateData["type"],
				value=self.lineEdit.text(),
				source=None if not self.value else self.value)
			if error:
				self.isError = True
				self.errorLine.setText(error)
			else:
				self.isError = False
				self.errorLine.setText("")
			self.ok.setDisabled(self.isError)
			self.updateIcon()

	def clearErrorLine(self):
		self.isError = False
		self.errorLine.setText("")
		self.ok.setDisabled(False)

	def updateIcon(self):
		pixmap = QPixmap(self.lineEdit.text())
		if not pixmap.width():
			self.icon.setText("-")
		else:
			pixmap = pixmap.scaled(*self.iconSize, Qt.KeepAspectRatio)
			self.icon.setPixmap(pixmap)
		self.title.setText(f"{pixmap.width()} x {pixmap.height()}")

	def updateLineEdit(self):
		self.lineEdit.setText(self.value)
		self.lineEdit.selectAll()
		self.lineEdit.setFocus()

	def willBeOpen(self, validateData=None, value="", action=None):
		self.validateData = validateData
		self.value = value
		self.action = action
		self.updateLineEdit()
		self.updateIcon()

	def willBeClosed(self):
		self.lineEdit.clearFocus()
		self.clearErrorLine()

	def eventFilter(self, object, event):
		if self.isOpen:
			res = self.ui.buttonHoverEvent(objects=[
				[self.openExplorerButton, assetsPath.folderHover, assetsPath.folder],
			], hoveredObject=object, event=event)
			if res:
				res = super(GetImagePathModalWidget, self).eventFilter(object, event)
			return res
		return False