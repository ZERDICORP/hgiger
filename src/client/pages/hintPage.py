from PyQt5.QtWidgets import QAction, QShortcut
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.components.contextMenuWidget import ContextMenuWidget
from client.components.tabWidget import TabWidget
from client.components.pageTextWidget import PageTextWidget
from client.components.pageTextWidgetFullScreen import PageTextWidgetFullScreen
from client.pages.pageWidget import PageWidget

class HintPage(PageWidget):
	def __init__(self, ui, hint):
		super(HintPage, self).__init__(ui)
		
		self.setStyleSheet("".join([
			styles.tabWidget,
			styles.menuButton
		]))

		self.hint = hint
		self.pageTextWidgetFullScreen = PageTextWidgetFullScreen(ui=self.ui)

		self.name = self.ui.createLabel(text=self.hint["name"], fontSize=20)
		self.name.setCursor(self.ui.CursorEdit)
		self.name.mouseDoubleClickEvent = lambda event: self.ui.inputModal.toggle(
			validateData={"type": self.ui.validator.validateType.ELEMENT_NAME},
			value=self.hint["name"],
			action=lambda value: self.ui.manager.reception(self.ui.manager.requestType.RENAME_HINT,
				hintId=self.hint["id"],
				newValue=value))
		self.tags = self.ui.createLabel(text=" ".join([f"#{tag}" for tag in self.hint["tags"]]), fontSize=11)
		self.tags.setMaximumHeight(self.ui.getFontHeight(fontSize=11))
		self.tags.setCursor(self.ui.CursorEdit)
		self.tags.mouseDoubleClickEvent = lambda event: self.ui.tagsModal.toggle(
			value=self.tags.text(),
			action=lambda tags: self.ui.manager.reception(self.ui.manager.requestType.EDIT_TAGS,
				newTags=tags))
		self.cancel = self.ui.createPushButton(iconPath=assetsPath.cancel, fixedSize=(30, 30), eventFilter=self, 
			action=self.cancelAction)
		self.tabWidget = TabWidget(ui=self.ui, createTabs=self.createTabs, contextMenu=self.tabContextMenu)
		self.createTabs()

		self.setLayout(self.ui.createVLayout([
			self.ui.createHLayout([
				self.name,
				self.cancel
			]),
			self.tags,
			self.tabWidget
		], alignment=Qt.AlignTop))

		QShortcut(QKeySequence("Ctrl+B"), self).activated.connect(self.cancelAction)

	def createTabs(self):
		for page in self.hint["pages"]:
			textEdit = PageTextWidget(ui=self.ui, text=page["content"], objectName=page["name"], 
				pageTextWidgetFullScreen=self.pageTextWidgetFullScreen)
			textEdit.mouseDoubleClickEvent = lambda event: self.ui.textModal.toggle(
				validateData={"type": self.ui.validator.validateType.ELEMENT_NAME},
				value=self.hint["pages"][self.tabWidget.currentIndex()]["content"],
				action=lambda value: self.ui.manager.reception(self.ui.manager.requestType.EDIT_PAGE_TEXT,
					pageId=self.tabWidget.currentIndex(),
					newValue=value))
			self.tabWidget.addTab(textEdit, QIcon(assetsPath.page), page["name"])

	def settingByHistory(self):
		self.ui.history.clearLast(self)
		tabIndex = self.getHistory()["tabIndex"]
		self.tabWidget.setCurrentIndex(tabIndex if tabIndex < len(self.hint["pages"]) else tabIndex - 1)

	def afterInit(self):
		self.tabWidget.currentChanged.connect(lambda index: 
			self.ui.history.updateTabIndex(self, index))

	def cancelAction(self):
		self.ui.openPage(
			pageCreator=lambda: self.ui.createHintsPage(self.ui.manager.currentCell["id"]))

	def deleteAction(self):
		self.cancelAction()
		self.ui.manager.reception(self.ui.manager.requestType.DELETE_HINT,
			hintId=self.hint["id"])

	def tabContextMenu(self, pos):
		contextMenu = ContextMenuWidget(self, self.ui.RobotoLight, [
			[QAction(QIcon(assetsPath.add), "Add", self), lambda: self.ui.inputModal.toggle(
				validateData={"type": self.ui.validator.validateType.SECTION_NAME},
				action=lambda pageName: self.ui.manager.reception(self.ui.manager.requestType.ADD_PAGE,
					currentPageId=self.tabWidget.currentIndex(),
					pageName=pageName)),
			False],
			[QAction(QIcon(assetsPath.reset), "Rename", self), lambda: self.ui.inputModal.toggle(
				validateData={"type": self.ui.validator.validateType.SECTION_NAME},
				value=self.tabWidget.currentName(),
				action=lambda pageName: self.ui.manager.reception(self.ui.manager.requestType.RENAME_PAGE,
					pageId=self.tabWidget.currentIndex(),
					newValue=pageName)), 
			False],
			[QAction(QIcon(assetsPath.delete), "Delete", self), lambda: self.ui.questionModal.toggle(
				question=f'Delete page "{self.tabWidget.currentName()}"?',
				action=lambda: self.ui.manager.reception(self.ui.manager.requestType.DELETE_PAGE,
					pageId=self.tabWidget.currentIndex())),
			bool(len(self.hint["pages"]) == 1)],
			[QAction(QIcon(assetsPath.swap), "Swap pages", self), lambda: self.ui.swapSectionsModal.toggle(
				sections=self.hint["pages"],
				currentIndex=self.tabWidget.currentIndex(),
				icon=assetsPath.page,
				action=lambda pages: self.ui.manager.reception(self.ui.manager.requestType.SWAP_PAGES,
					pages=pages)), 
			bool(len(self.hint["pages"]) == 1)],
		])
		contextMenu.exec_(self.tabWidget.mapToGlobal(pos))

	def contextMenuEvent(self, event):
		contextMenu = ContextMenuWidget(self, self.ui.RobotoLight, [
			[QAction(QIcon(assetsPath.rename), "Rename", self), lambda: self.ui.inputModal.toggle(
				validateData={"type": self.ui.validator.validateType.ELEMENT_NAME},
				value=self.hint["name"],
				action=lambda text: self.ui.manager.reception(self.ui.manager.requestType.RENAME_HINT,
					hintId=self.hint["id"],
					newValue=text)),
			False],
			[QAction(QIcon(assetsPath.delete), "Delete", self), lambda: self.ui.questionModal.toggle(
				question=f'Delete hint "{self.ui.truncate(string=self.hint["name"], length=30)}"?', 
				action=self.deleteAction), 
			False],
		])
		contextMenu.exec_(self.mapToGlobal(event.pos()))

	def eventFilter(self, object, event):
		return self.ui.buttonHoverEvent(objects=[
			[self.cancel, assetsPath.cancelHover, assetsPath.cancel],
		], hoveredObject=object, event=event)
