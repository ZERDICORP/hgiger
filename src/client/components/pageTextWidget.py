from PyQt5.QtWidgets import QAction, QPlainTextEdit, QApplication
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.components.contextMenuWidget import ContextMenuWidget

class PageTextWidget(QPlainTextEdit):
	def __init__(self, ui, text, objectName, pageTextWidgetFullScreen):
		super(PageTextWidget, self).__init__()
		
		self.setPlaceholderText("Double click to edit..")
		self.setReadOnly(True)
		self.setObjectName(objectName)
		self.setTabStopDistance(40)
		self.setStyleSheet(styles.textEdit)

		self.ui = ui
		self.text = text
		self.pageTextWidgetFullScreen = pageTextWidgetFullScreen

		self.setFont(QFont(self.ui.RobotoLight, 12))
		self.setPlainText(self.text)

	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton and (QApplication.keyboardModifiers() & Qt.ControlModifier) == Qt.ControlModifier:
			self.pageTextWidgetFullScreen.showFullScreen(text=self.text)
		super(PageTextWidget, self).mousePressEvent(event)

	def contextMenuEvent(self, event):
		contextMenu = ContextMenuWidget(self, self.ui.RobotoLight, [
			[QAction(QIcon(assetsPath.resize), "Full screen", self), lambda: self.pageTextWidgetFullScreen.showFullScreen(text=self.text), 
			False],
		])
		contextMenu.exec_(self.mapToGlobal(event.pos()))