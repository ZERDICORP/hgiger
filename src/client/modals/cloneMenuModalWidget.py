from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.modals.modalWidget import ModalWidget

class CloneMenuModalWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(CloneMenuModalWidget, self).__init__(parent, ui)

		self.setStyleSheet("".join([
			styles.cloneMenu,
			styles.menuButton
		]))

		self.title = self.ui.createLabel(text="Clone Menu", objectName="title", alignment=Qt.AlignCenter, fontSize=20)
		self.close = self.ui.createPushButton(iconPath=assetsPath.delete, action=self.toggle, fixedSize=(30, 30), 
			eventFilter=self)
		self.telegramButton = self.ui.createPushButton(iconPath=assetsPath.telegram, text=" Clone to Telegram", objectName="button", fontSize=12,
			action=lambda: self.openOtherModal(self.ui.telegramModal.toggle), eventFilter=self)

		self.mainLayout.addLayout(self.ui.createHLayout([self.title, self.close]))
		self.mainLayout.addLayout(self.ui.createVLayout([self.telegramButton]))
		self.mainLayout.addStretch(1)

		self.setMinimumHeight((int)(self.ui.WProperties[0][1] / 100 * 80))
		self.setMinimumWidth((int)(self.ui.WProperties[0][0] / 100 * 50))

		self.parent.setChild(self, alignment=Qt.AlignCenter)

	def eventFilter(self, object, event):
		return self.ui.buttonHoverEvent(objects=[
			[self.close, assetsPath.deleteHover, assetsPath.delete],
			[self.telegramButton, assetsPath.telegramHover, assetsPath.telegram],
		], hoveredObject=object, event=event)
