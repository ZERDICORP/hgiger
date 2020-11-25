import math
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QAction, QShortcut
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence
from PyQt5.QtCore import Qt, QRect
from client.tools.staticManager import assetsPath, styles
from client.components.contextMenuWidget import ContextMenuWidget

class ImageWidgetFullScreen(QGraphicsView):
	def __init__(self, ui, path):
		super(ImageWidgetFullScreen, self).__init__()
		
		self.setAlignment(Qt.AlignCenter)
		self.setStyleSheet("".join([
			styles.window, 
			styles.graphicsView
		]))

		self.ui = ui

		self.scene = QGraphicsScene()
		self.scene.addPixmap(QPixmap(path))

		self.setGeometry(QRect(0, 0, *self.ui.sWH))
		self.setScene(self.scene)

		QShortcut(QKeySequence("Escape"), self).activated.connect(self.close)

	def wheelEvent(self, event):
		if event.modifiers() == Qt.ControlModifier:
			self.scale(math.pow(2, event.angleDelta().y() / 1000), math.pow(2, event.angleDelta().y() / 1000))
		else:
			return QGraphicsView.wheelEvent(self, event)

	def contextMenuEvent(self, event):
		contextMenu = ContextMenuWidget(self, self.ui.RobotoLight, [
			[QAction(QIcon(assetsPath.delete), "Close", self), self.close, False]
		])
		contextMenu.exec_(self.mapToGlobal(event.pos()))