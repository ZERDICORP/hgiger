from PyQt5.QtWidgets import QListWidget, QAction
from PyQt5.QtGui import QIcon
from client.tools.staticManager import assetsPath
from client.components.cellWidget import CellWidget
from client.components.tabWidget import TabWidget
from client.components.contextMenuWidget import ContextMenuWidget
from client.pages.pageWidget import PageWidget

class CellsPage(PageWidget):
	def __init__(self, ui, sections, cells):
		super(CellsPage, self).__init__(ui)
		
		self.sections, self.cells = sections, cells
		self.sortedCells = [[cell for cell in self.cells if cell["section"] == section["name"]] for section in self.sections]
		
		self.tabWidget = TabWidget(ui=self.ui, createTabs=self.createTabs, contextMenu=self.contextMenu)
		self.createTabs()

		self.setLayout(self.ui.createVLayout([self.tabWidget]))
		
	def createTabs(self):
		for i, section in enumerate(self.sections):
			if self.sortedCells[i]:
				widget = self.ui.createList()
				widget.verticalScrollBar().valueChanged.connect(lambda value:
					self.ui.history.updateScrollLevel(self, value))
				for cell in self.sortedCells[i]:
					self.ui.insertItemToList(widget, CellWidget(ui=self.ui, cell=cell))
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
			self.tabWidget.currentWidget().verticalScrollBar().setValue(
				self.getHistory()["scrollLevel"])

	def afterInit(self):
		self.tabWidget.currentChanged.connect(lambda index: 
			self.ui.history.updateTabIndex(self, index))

	def contextMenu(self, pos):
		contextMenu = ContextMenuWidget(self, self.ui.RobotoLight, [
			[QAction(QIcon(assetsPath.rename), "Rename", self), lambda: self.ui.inputModal.toggle(
				validateData={"type": self.ui.validator.validateType.SECTION_NAME},
				value=self.tabWidget.currentName(),
				action=lambda text: self.ui.manager.reception(self.ui.manager.requestType.RENAME_CELL_SECTION,
					sectionId=self.tabWidget.currentIndex(),
					newValue=text)), 
			False],
			[QAction(QIcon(assetsPath.image), "Reicon", self), lambda: self.ui.getImagePathModal.toggle(
				validateData={"type": self.ui.validator.validateType.IMAGE_PATH},
				value=self.tabWidget.currentIcon(),
				action=lambda text: self.ui.manager.reception(self.ui.manager.requestType.REICON_CELL_SECTION,
					sectionId=self.tabWidget.currentIndex(),
					newValue=text)),
			False],
			[QAction(QIcon(assetsPath.delete), "Delete", self), lambda: self.ui.questionModal.toggle(
				f'Delete section "{self.tabWidget.currentName()}"?', lambda: self.ui.manager.reception(self.ui.manager.requestType.DELETE_CELL_SECTION,
					sectionId=self.tabWidget.currentIndex())),
			bool(len(self.sections) == 1)],
			[QAction(QIcon(assetsPath.swap), "Swap sections", self), lambda: self.ui.swapSectionsModal.toggle(
				sections=self.sections,
				currentIndex=self.tabWidget.currentIndex(),
				action=lambda sections: self.ui.manager.reception(self.ui.manager.requestType.SWAP_CELL_SECTIONS,
					sections=sections)),
			bool(len(self.sections) == 1)],
			[QAction(QIcon(assetsPath.add), "Add section", self), lambda: self.ui.addSectionModal.toggle(
				requestData={"type": self.ui.manager.requestType.ADD_CELL_SECTION},
				validateData={
					"nameType": self.ui.validator.validateType.SECTION_NAME,
					"imageType": self.ui.validator.validateType.IMAGE_PATH
				},
				currentSectionId=self.tabWidget.currentIndex(),
				sections=[section["name"] for section in self.sections]), 
			False],
			[QAction(QIcon(assetsPath.add), "Add cell", self), lambda: self.ui.addElementModal.toggle(
				validateData={"type": self.ui.validator.validateType.ELEMENT_NAME},
				currentSection=self.tabWidget.currentName(),
				action=lambda cellName: self.ui.manager.reception(self.ui.manager.requestType.ADD_CELL,
					cellName=cellName,
					section=self.tabWidget.currentName())),
			False],
		])
		contextMenu.exec_(self.mapToGlobal(pos))