from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.modals.modalWidget import ModalWidget

class InfoModalWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(InfoModalWidget, self).__init__(parent, ui)
		
		self.setStyleSheet("".join([
			styles.menuButton
		]))
		
		self.info = self.ui.createLabel(alignment=Qt.AlignCenter, objectName="question", fontSize=18)
		self.ok = self.ui.createPushButton(iconPath=assetsPath.success, action=self.toggle, fixedSize=(30, 30), 
			eventFilter=self)

		self.mainLayout.addLayout(self.ui.createVLayout([
			self.info,
			self.ui.createHLayout([self.ok], alignment=Qt.AlignCenter)
		]))

		self.parent.setChild(self)

	def willBeOpen(self, info):
		self.info.setText(info)