from PyQt5.QtWidgets import QWidget, QAction
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.components.contextMenuWidget import ContextMenuWidget

class CellWidget(QWidget):
	def __init__ (self, ui, cell):
		super(CellWidget, self).__init__()

		self.setStyleSheet(styles.listItem)

		self.ui = ui
		self.cell = cell

		self.icon = self.ui.createLabel()
		self.icon.setScaledContents(True)
		self.icon.setPixmap(QPixmap(assetsPath.cell).scaled(35, 40))
		
		self.name = self.ui.createLabel(text=self.cell["name"], objectName="name", fontSize=14, 
			alignment=Qt.AlignVCenter)
		self.name.setMinimumHeight(40)

		self.setLayout(self.ui.createHLayout([
			self.icon,
			self.ui.STRETCHi,
			self.name
		]))
		self.setCursor(self.ui.CursorPointer)

	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.ui.openPage(pageCreator=lambda: self.ui.createHintsPage(self.cell["id"]))

	def contextMenuEvent(self, event):
		contextMenu = ContextMenuWidget(self, self.ui.RobotoLight, [
			[QAction(QIcon(assetsPath.rename), "Rename", self), lambda: self.ui.inputModal.toggle(
				validateData={"type": self.ui.validator.validateType.ELEMENT_NAME},
				value=self.cell["name"],
				action=lambda text: self.ui.manager.reception(self.ui.manager.requestType.RENAME_CELL,
					cellId=self.cell["id"],
					newValue=text)),
			False],
			[QAction(QIcon(assetsPath.move), "Move", self), lambda: self.ui.moveCellModal.toggle(
				objectName=self.cell["name"],
				objectId=self.cell["id"],
				objectSection=self.cell["section"]),
			not len(self.ui.manager.cellSections) > 1],
			[QAction(QIcon(assetsPath.delete), "Delete", self), lambda: self.ui.questionModal.toggle(f'Delete cell "{self.cell["name"]}"?', 
				lambda: self.ui.manager.reception(self.ui.manager.requestType.DELETE_CELL,
					cellId=self.cell["id"])), 
			False]
		])
		contextMenu.exec_(self.mapToGlobal(event.pos()))