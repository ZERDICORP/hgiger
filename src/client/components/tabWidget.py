from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtGui import QFont
from client.tools.staticManager import styles

class TabWidget(QTabWidget):
	def __init__(self, ui, createTabs, contextMenu):
		super(TabWidget, self).__init__()
		
		self.setStyleSheet("\n".join([
			styles.tabWidget,
			styles.listWidget
		]))

		self.ui = ui
		self.createTabs = createTabs
		self.contextMenu = contextMenu

		self.tabBar().setCursor(self.ui.CursorPointer)
		self.tabBar().setFont(QFont(self.ui.RobotoLight, 12))

	def currentName(self):
		return self.currentWidget().objectName().split(" % ")[0]

	def currentIcon(self):
		return self.currentWidget().objectName().split(" % ")[1]

	def contextMenuEvent(self, event):
		self.contextMenu(event.pos())