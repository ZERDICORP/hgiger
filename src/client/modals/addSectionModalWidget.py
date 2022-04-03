from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.modals.modalWidget import ModalWidget

class AddSectionModalWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(AddSectionModalWidget, self).__init__(parent, ui)
		
		self.setStyleSheet("".join([
			styles.lineEdit,
			styles.menuButton,
			styles.validator
		]))

		self.validateData, self.requestData = {}, {}
		self.iconSize = (30, 30)

		self.icon = self.ui.createPixmap(objectName="icon", fontSize=10)
		self.title = self.ui.createLabel(fontSize=12, objectName="size", alignment=Qt.AlignHCenter)
		self.nameEdit = self.ui.createLineEdit(placeholder="Enter name..", fontSize=12,
			alignment=Qt.AlignCenter, returnAction=self.readyToAction, inputAction=self.updateErrorLine)
		self.nameErrorLine = self.ui.createLabel(objectName="errorLine", fontSize=8, alignment=Qt.AlignCenter)
		self.iconEdit = self.ui.createLineEdit(text=self.ui.defaultSectionIcon, placeholder="Enter icon path..",
			alignment=Qt.AlignCenter, fontSize=12, returnAction=self.nameEdit.setFocus, inputAction=self.updateErrorLine)
		self.iconErrorLine = self.ui.createLabel(objectName="errorLine", fontSize=8, alignment=Qt.AlignCenter)

		self.mainLayout.addLayout(self.ui.createVLayout([
			self.ui.createVLayout([
				self.title,
				self.ui.createHLayout([self.icon], alignment=Qt.AlignCenter),
				self.iconEdit,
				self.iconErrorLine
			]),
			self.ui.createVLayout([self.nameEdit, self.nameErrorLine])
		]))

		self.openExplorerButton = self.ui.createPushButton(iconPath=assetsPath.folder, action=self.openExplorer, fixedSize=(30, 30), 
			eventFilter=self)
		self.defaultValueButton = self.ui.createPushButton(iconPath=assetsPath.default, action=lambda: self.iconEdit.setText(self.ui.defaultSectionIcon), fixedSize=(30, 30), 
			eventFilter=self)
		self.setYesNoButtons(yesAction=self.readyToAction, between=[self.openExplorerButton, self.defaultValueButton])

		self.parent.setChild(self)

	def readyToAction(self):
		self.updateErrorLine()
		if not self.isError:
			self.ui.manager.reception(self.requestData["type"],
				currentSectionId=self.currentSectionId,
				sectionName=self.nameEdit.text(),
				sectionIcon=self.iconEdit.text())
			self.toggle()

	def updateIconErrorLine(self):
		error = self.ui.validator.validate(self.validateData["imageType"],
			value=self.iconEdit.text(),
			source=None)
		self.iconErrorLine.setText(error) if error else self.iconErrorLine.setText("")
		return bool(error)

	def updateNameErrorLine(self):
		error = self.ui.validator.validate(self.validateData["nameType"],
			value=self.nameEdit.text(),
			source=None,
			sections=self.sections)
		self.nameErrorLine.setText(error) if error else self.nameErrorLine.setText("")
		return bool(error)

	def updateErrorLine(self):
		if self.isOpen:
			self.isError = bool(sum([self.updateIconErrorLine(), self.updateNameErrorLine()]))
			self.ok.setDisabled(self.isError)
			self.updateIcon()

	def updateIcon(self):
		pixmap = QPixmap(self.iconEdit.text())
		if not pixmap.width():
			self.icon.setText("-")
		else:
			pixmap = pixmap.scaled(*self.iconSize, Qt.KeepAspectRatio)
			self.icon.setPixmap(pixmap)
		self.title.setText(f"{pixmap.width()} x {pixmap.height()}")

	def openExplorer(self):
		path = self.ui.openExplorer()
		if path:
			self.iconEdit.setText(path)

	def clearErrorLine(self):
		self.isError = False
		self.nameErrorLine.setText("")
		self.iconErrorLine.setText("")
		self.ok.setDisabled(False)

	def clearLineEdit(self):
		self.iconEdit.setText(self.ui.defaultSectionIcon)
		self.iconEdit.clearFocus()
		self.nameEdit.clear()
		self.nameEdit.clearFocus()

	def willBeOpen(self, requestData, validateData, currentSectionId, sections):
		self.requestData = requestData
		self.validateData = validateData
		self.currentSectionId = currentSectionId
		self.sections = sections
		self.updateIcon()
		self.nameEdit.setFocus()

	def willBeClosed(self):
		self.clearLineEdit()
		self.clearErrorLine()

	def eventFilter(self, object, event):
		if self.isOpen:
			res = self.ui.buttonHoverEvent(objects=[
				[self.openExplorerButton, assetsPath.folderHover, assetsPath.folder],
				[self.defaultValueButton, assetsPath.defaultHover, assetsPath.default],
			], hoveredObject=object, event=event)
			if res:
				res = super(AddSectionModalWidget, self).eventFilter(object, event)
			return res
		return False