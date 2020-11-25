from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.modals.modalWidget import ModalWidget

class MoveSectionModalWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(MoveSectionModalWidget, self).__init__(parent, ui)
		
		self.setStyleSheet("".join([
			styles.menuButton,
			styles.tabWidget,
			styles.validator
		]))

		self.tabWidget = self.ui.createTabWidget()
		self.tabWidget.setMovable(True)
		self.tabWidget.tabBar().currentChanged.connect(self.updateErrorLine)
		self.errorLine = self.ui.createLabel(objectName="errorLine", fontSize=8, alignment=Qt.AlignCenter)

		self.mainLayout.addLayout(self.ui.createVLayout([
			self.tabWidget,
			self.errorLine
		]))
		self.setYesNoButtons(yesAction=self.readyToAction)

		self.parent.setChild(self)

	def readyToAction(self):
		self.updateErrorLine()
		if not self.isError:
			self.action(self.newSections)
			self.toggle()

	def updateErrorLine(self):
		if self.isOpen:
			self.newSections = self.getSections()
			error = self.ui.validator.validate(self.ui.validator.validateType.ARR,
				value=self.newSections,
				source=[section["name"] for section in self.sections])
			self.errorLine.setText(error if error else "")
			self.isError = bool(error)
			self.ok.setDisabled(self.isError)

	def getSections(self):
		return [self.tabWidget.widget(index).objectName() for index in range(self.tabWidget.count())]
		
	def updateTabWidget(self):
		self.tabWidget.clear()
		for i, section in enumerate(self.sections):
			self.tabWidget.addTab(QWidget(objectName=section["name"]), QIcon(self.icon if self.icon else section["icon"]), section["name"])

	def willBeOpen(self, sections=None, icon=None, action=None):
		self.sections = sections
		self.icon = icon
		self.action = action
		self.updateTabWidget()