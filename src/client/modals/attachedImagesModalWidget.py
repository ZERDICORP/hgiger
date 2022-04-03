from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.components.imageWidget import ImageWidget
from client.components.contextMenuWidget import ContextMenuWidget
from client.modals.modalWidget import ModalWidget

class AttachedImagesModalWidget(ModalWidget):
	def __init__(self, parent, pageWidget, ui, images):
		super(AttachedImagesModalWidget, self).__init__(parent, ui)
		
		self.setMinimumHeight((int)(self.ui.WProperties[0][1] / 100 * 80))
		self.setMinimumWidth((int)(self.ui.WProperties[0][0] / 100 * 60))
		self.setStyleSheet("".join([
			styles.listWidget,
			styles.menuButton,
			styles.attachedImagesWidget
		]))

		self.pageWidget = pageWidget

		self.title = self.ui.createLabel(text="Attached Images", fontSize=20, alignment=Qt.AlignCenter)
		self.close = self.ui.createPushButton(iconPath=assetsPath.delete, fixedSize=(30, 30), action=self.toggle, eventFilter=self)
		
		self.mainLayout.addLayout(self.ui.createHLayout([self.title, self.close]))

		if images:
			self.imageList = self.ui.createList()
			for i, fileName in enumerate(images):
				self.ui.insertItemToList(list=self.imageList, 
					item=ImageWidget(ui=self.ui, width=self.width(), fileName=fileName, id=i))
			self.mainLayout.addWidget(self.imageList)
		else:
			self.mainLayout.addWidget(self.ui.createZero(fontSize=40))

		self.parent.setChild(self, alignment=Qt.AlignCenter)

	def contextMenuEvent(self, event):
		contextMenu = ContextMenuWidget(self, self.ui.RobotoLight, [
			[QAction(QIcon(assetsPath.add), "Add image", self), lambda: self.ui.getImagePathModal.toggle(
				validateData={"type": self.ui.validator.validateType.IMAGE_PATH},
				action=lambda imagePath: self.ui.manager.reception(self.ui.manager.requestType.ADD_IMAGE,
					imagePath=imagePath)),
			False],
		])
		contextMenu.exec_(self.mapToGlobal(event.pos()))

	def toggle(self, *args, **kwargs):
		super(AttachedImagesModalWidget, self).toggle(*args, **kwargs)
		self.ui.history.updateAttachedImages(self.pageWidget, self.isOpen)

	def eventFilter(self, object, event):
		return self.ui.buttonHoverEvent(objects=[
			[self.close, assetsPath.deleteHover, assetsPath.delete]
		], hoveredObject=object, event=event)
