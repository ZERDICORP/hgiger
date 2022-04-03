from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.tools.tagFinderTools import TagFinderTools
from client.components.contextMenuWidget import ContextMenuWidget
from client.components.hintWidget import HintWidget
from client.modals.modalWidget import ModalWidget
from modules.strDiff import strDiff

class TagFinderWidget(ModalWidget, TagFinderTools):
	def __init__(self, parent, pageWidget, ui, tabWidget, sections, hints):
		super(TagFinderWidget, self).__init__(parent, ui)
		
		self.setStyleSheet("".join([
			styles.menuButton,
			styles.listWidget,
			styles.lineEdit,
			styles.comboBox,
			styles.tagFinder
		]))
		
		self.pageWidget = pageWidget
		self.tabWidget = tabWidget
		self.sections, self.hints = sections, hints
		self.tags = self.getTags()
		self.inGlobalScope = True
		self.findedTags = []
				
		self.title = self.ui.createLabel(text="Tag Finder", fontSize=20)
		self.menuButton = self.ui.createPushButton(iconPath=assetsPath.menu, action=self.openMenu, fixedSize=(30, 30), 
			eventFilter=self)		
		self.tagList = self.ui.createComboBox(items=self.tags, activated=self.find) 
		self.lineEdit = self.ui.createLineEdit(placeholder="Enter tag..", returnAction=self.find,
			inputAction=lambda text: self.onKeyPressed(text.split(" ")[-1]))
		self.scopeInfo = self.ui.createLabel(text="Global scope", alignment=Qt.AlignRight, fontSize=10)
		self.resultList = self.ui.createList()
		self.resultList.verticalScrollBar().valueChanged.connect(lambda value:
			self.ui.history.updateTagScrollLevel(self.pageWidget, value))

		self.mainLayout.addLayout(self.ui.createHLayout([self.title, self.menuButton]))
		self.mainLayout.addWidget(self.tagList)
		self.mainLayout.addWidget(self.lineEdit)
		self.mainLayout.addWidget(self.scopeInfo)
		self.mainLayout.addWidget(self.resultList)
		
		self.setMinimumHeight((int)(self.ui.WProperties[0][1] / 100 * 80))
		self.setMinimumWidth((int)(self.ui.WProperties[0][0] / 100 * 80))

		self.parent.setChild(self, alignment=Qt.AlignCenter)

	def settingByHistory(self, history):
		self.inGlobalScope = not history["globalScope"]
		self.toggleGlobalScope()
		self.lineEdit.setText(history["tagLine"])
		self.find()
		self.showEvent = lambda event: self.resultList.verticalScrollBar().setValue(history["tagScrollLevel"])
		self.toggle()

	def showResult(self, hints):
		self.resultList.clear()
		for hint in hints:
			self.ui.insertItemToList(self.resultList, 
				HintWidget(ui=self.ui, hint=hint, findedTags=self.findedTags, parentWidth=self.width()))

	def find(self):
		self.setTagToLineEdit(self.tagList.currentText())
		self.findedTags = self.lineEdit.text().split(" ")
		self.showResult(self.findByTags(tags=self.findedTags))

	def setTagToLineEdit(self, tag):
		text = " ".join([*self.lineEdit.text().split(" ")[:-1], tag])
		self.lineEdit.setText(text)
		self.ui.history.updateTagLine(self.pageWidget, text)

	def onKeyPressed(self, text):
		top = [0, None]
		for tag in self.tags:
			diff = strDiff(tag, text)
			if diff > top[0]:
				top = [diff, tag]
		self.tagList.setCurrentText(top[1])

	def resetTaglist(self):
		currentText = self.tagList.currentText()
		self.tagList.clear()
		self.tags = self.getTags(self.inGlobalScope)
		self.tagList.addItems(self.tags)
		self.tagList.setCurrentText(currentText)

	def updateScopeInfo(self):
		self.scopeInfo.setText("In Global scope" if self.inGlobalScope else f"In \"{self.tabWidget.currentName()}\" section")

	def toggleGlobalScope(self):
		self.inGlobalScope = not self.inGlobalScope
		self.resetTaglist()
		self.updateScopeInfo()
		self.ui.history.updateGlobalScope(self.pageWidget, self.inGlobalScope)

	def willBeOpen(self):
		self.lineEdit.setFocus()
		self.resetTaglist()
		self.updateScopeInfo()

	def clear(self):
		self.findedTags = []
		self.lineEdit.setText("")
		self.tagList.setCurrentIndex(0)
		self.resultList.clear()

	def willBeClosed(self):
		self.lineEdit.clearFocus()
		self.clear()

	def toggle(self, *args, **kwargs):
		super(TagFinderWidget, self).toggle(*args, **kwargs)
		self.ui.history.updateTagFinder(self.pageWidget, self.isOpen)

	def openMenu(self):
		contextMenu = ContextMenuWidget(self, self.ui.RobotoLight, [
			[QAction(QIcon(assetsPath.delete), "Close", self), self.toggle, False],
			[QAction(QIcon(assetsPath.success if self.inGlobalScope else assetsPath.delete), "Global scope", self, checkable=True), 
				self.toggleGlobalScope, False]
		])
		contextMenu.exec_(self.mapToGlobal(self.menuButton.geometry().bottomRight()))

	def eventFilter(self, object, event):
		return self.ui.buttonHoverEvent(objects=[
			[self.menuButton, assetsPath.menuHover, assetsPath.menu]
		], hoveredObject=object, event=event)
