from PyQt5.QtWidgets import QPlainTextEdit, QShortcut, QAction
from PyQt5.QtGui import QKeySequence, QFont, QIcon
from PyQt5.QtCore import QRect
from client.tools.staticManager import assetsPath, styles
from client.components.contextMenuWidget import ContextMenuWidget

class PageTextWidgetFullScreen(QPlainTextEdit):
	def __init__(self, ui):
		super(PageTextWidgetFullScreen, self).__init__()

		self.setReadOnly(True)
		self.setTabStopDistance(40)
		self.setStyleSheet("".join([
			styles.window,
			styles.textEdit,
			styles.textEditFS
		]))
		
		self.ui = ui

		self.setFont(QFont(self.ui.RobotoLight, 14))
		self.setGeometry(QRect(0, 0, *self.ui.sWH))

		QShortcut(QKeySequence("Escape"), self).activated.connect(self.close)

	def showFullScreen(self, text):
		self.setPlainText(text)
		super(PageTextWidgetFullScreen, self).showFullScreen()

	def contextMenuEvent(self, event):
		contextMenu = ContextMenuWidget(self, self.ui.RobotoLight, [
			[QAction(QIcon(assetsPath.delete), "Close", self), self.close, False]
		])
		contextMenu.exec_(self.mapToGlobal(event.pos()))