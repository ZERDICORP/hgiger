from PyQt5.QtWidgets import QLabel, QAction
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.components.contextMenuWidget import ContextMenuWidget
from client.components.imageWidgetFullScreen import ImageWidgetFullScreen

class ImageWidget(QLabel):
	def __init__(self, ui, width, fileName, id):
		super(ImageWidget, self).__init__()
		
		self.setAlignment(Qt.AlignCenter)
		self.setStyleSheet(styles.imageWidget)

		self.ui = ui
		self.width = int(width / 100 * 80)
		self.path = f"{self.ui.manager.baseImagePath}/{fileName}" 
		self.id = id
		self.imageName = self.ui.manager.imageManager.withoutSeparator(fileName) if "____" in fileName else fileName
		self.imageWidgetFullScreen = ImageWidgetFullScreen(self.ui, self.path)
		self.pixmap = QPixmap(self.path).scaled(self.width, self.width, Qt.KeepAspectRatio)

		self.setToolTip(self.imageName)
		self.setPixmap(self.pixmap)
		self.setCursor(self.ui.CursorPointer)

	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.imageWidgetFullScreen.showFullScreen()

	def contextMenuEvent(self, event):
		contextMenu = ContextMenuWidget(self, self.ui.RobotoLight, [
			[QAction(QIcon(assetsPath.delete), "Delete", self), lambda: self.ui.questionModal.toggle(
				question=f'Delete image "{self.ui.truncate(self.imageName, 30)}"?', 
				action=lambda: self.ui.manager.reception(self.ui.manager.requestType.DELETE_IMAGE,
					imageId=self.id)), 
			False]
		])
		contextMenu.exec_(self.mapToGlobal(event.pos()))
