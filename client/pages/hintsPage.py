from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QAbstractItemView, QShortcut, QMenu, QAction, QLineEdit
from PyQt5.QtGui import QIcon, QKeySequence, QFont
from client.tools.staticManager import assetsPath, styles
from client.components.hintWidget import HintWidget
from client.components.tabWidget import TabWidget
from client.components.tagFinderWidget import TagFinderWidget
from client.components.contextMenuWidget import ContextMenuWidget
from client.components.smokeWidget import SmokeWidget
from client.pages.pageWidget import PageWidget

class HintsPage(PageWidget):
	def __init__(self, ui, sections, hints):
		super(HintsPage, self).__init__(ui)

		self.setStyleSheet(styles.menuButton)

		self.sections, self.hints = sections, hints
		self.sortedHints = [[hint for hint in self.hints if hint["section"] == section["name"]] for section in self.sections]

		self.tabWidget = TabWidget(ui=self.ui, createTabs=self.createTabs, contextMenu=self.contextMenu)
		self.createTabs()

		self.setLayout(self.ui.createVLayout([self.tabWidget]))

		QShortcut(QKeySequence("Ctrl+B"), self).activated.connect(self.goBack)

	def createTabs(self):
		for i, section in enumerate(self.sections):
			if self.sortedHints[i]:
				widget = self.ui.createList()
				widget.verticalScrollBar().valueChanged.connect(lambda value:
					self.ui.history.updateScrollLevel(self, value))
				for hint in self.sortedHints[i]:
					self.ui.insertItemToList(widget, HintWidget(ui=self.ui, hint=hint, findedTags=None, parentWidth=self.tabWidget.width()))
			else:
				widget = self.ui.createZero(fontSize=40)
			widgetIcon = self.ui.byDefaultIcon(section["icon"])
			widget.setObjectName(f"{section['name']} % {widgetIcon}")
			self.tabWidget.addTab(widget, QIcon(widgetIcon), section["name"])

	def settingByHistory(self):
		self.ui.history.clearLast(self)
		tabIndex = self.getHistory()["tabIndex"]
		self.tabWidget.setCurrentIndex(tabIndex if tabIndex < len(self.sections) else tabIndex - 1)
		if type(self.tabWidget.currentWidget()) == QListWidget:
			self.tabWidget.showEvent = lambda event: self.tabWidget.currentWidget().verticalScrollBar().setValue(
				self.getHistory()["scrollLevel"])

	def afterInit(self):
		self.setTagFinder()
		self.setCancelButton()
		self.tabWidget.currentChanged.connect(lambda index: self.ui.history.updateTabIndex(self, index))

	def goBack(self):
		self.ui.openPage(pageCreator=self.ui.createCellsPage)

	def setTagFinder(self):
		self.tagFinder = TagFinderWidget(parent=self.ui.createSmokeWidget(), pageWidget=self, ui=self.ui, tabWidget=self.tabWidget, 
			sections=self.sections, hints=self.hints)
		QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.tagFinder.toggle)
		if self.getHistory()["tagFinder"]:
			self.tagFinder.settingByHistory(self.getHistory())

	def setCancelButton(self):
		self.cancel = self.ui.createPushButton(iconPath=assetsPath.cancel, fixedSize=(30, 30), eventFilter=self, 
			action=lambda: self.goBack())
		self.cancel.setParent(self.tabWidget)
		self.cancel.move(self.ui.WProperties[0][0] - 50, self.ui.WProperties[0][1] - 50)

	def contextMenu(self, pos):
		contextMenu = ContextMenuWidget(self, self.ui.RobotoLight, [
			[QAction(QIcon(assetsPath.rename), "Rename", self), lambda: self.ui.inputModal.toggle(
				validateData={"type": self.ui.validator.validateType.SECTION_NAME},
				value=self.tabWidget.currentName(),
				action=lambda text: self.ui.manager.reception(self.ui.manager.requestType.RENAME_HINT_SECTION,
					sectionId=self.tabWidget.currentIndex(),
					newValue=text)), 
			False],
			[QAction(QIcon(assetsPath.image), "Reicon", self), lambda: self.ui.getImagePathModal.toggle(
				validateData={"type": self.ui.validator.validateType.IMAGE_PATH},
				value=self.tabWidget.currentIcon(),
				action=lambda text: self.ui.manager.reception(self.ui.manager.requestType.REICON_HINT_SECTION,
					sectionId=self.tabWidget.currentIndex(),
					newValue=text)), 
			False],
			[QAction(QIcon(assetsPath.delete), "Delete", self), lambda: self.ui.questionModal.toggle(
				f'Delete section "{self.tabWidget.currentName()}"?', lambda: self.ui.manager.reception(self.ui.manager.requestType.DELETE_HINT_SECTION,
					sectionId=self.tabWidget.currentIndex())),
			bool(len(self.sections) == 1)],
			[QAction(QIcon(assetsPath.swap), "Swap sections", self), lambda: self.ui.swapSectionsModal.toggle(
				sections=self.sections,
				currentIndex=self.tabWidget.currentIndex(),
				action=lambda sections: self.ui.manager.reception(self.ui.manager.requestType.SWAP_HINT_SECTIONS,
					sections=sections)),
			bool(len(self.sections) == 1)],
			[QAction(QIcon(assetsPath.add), "Add section", self), lambda: self.ui.addSectionModal.toggle(
				requestData={"type": self.ui.manager.requestType.ADD_HINT_SECTION},
				validateData={
					"nameType": self.ui.validator.validateType.SECTION_NAME,
					"imageType": self.ui.validator.validateType.IMAGE_PATH
				},
				currentSectionId=self.tabWidget.currentIndex(),
				sections=[section["name"] for section in self.sections]), 
			False],
			[QAction(QIcon(assetsPath.add), "Add hint", self), lambda: self.ui.addElementModal.toggle(
				validateData={"type": self.ui.validator.validateType.ELEMENT_NAME},
				currentSection=self.tabWidget.currentName(),
				action=lambda hintName: self.ui.manager.reception(self.ui.manager.requestType.ADD_HINT,
					hintName=hintName,
					section=self.tabWidget.currentName())), 
			False],
		])
		contextMenu.exec_(self.mapToGlobal(pos))

	def eventFilter(self, object, event):
		return self.ui.buttonHoverEvent(objects=[
			[self.cancel, assetsPath.cancelHover, assetsPath.cancel],
		], hoveredObject=object, event=event)