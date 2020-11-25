from PyQt5.QtWidgets import QFrame
from client.tools.staticManager import assetsPath

class ModalWidget(QFrame):
	def __init__(self, parent, ui):
		super(ModalWidget, self).__init__(parent)
		
		self.parent = parent
		self.ui = ui
		self.isOpen = False
		self.isError = False

		self.mainLayout = self.ui.createVLayout()

		self.setLayout(self.mainLayout)

	def toggle(self, *args, **kwargs):
		if not self.isOpen:
			self.willBeOpen(*args, **kwargs)
			self.parent.open()
		else:
			self.willBeClosed()
			self.parent.close()
		self.isOpen = not self.isOpen

	def setYesNoButtons(self, yesAction=None, between=[]):
		self.close = self.ui.createPushButton(iconPath=assetsPath.delete, action=self.toggle, fixedSize=(30, 30), 
			eventFilter=self)
		self.ok = self.ui.createPushButton(iconPath=assetsPath.success, action=yesAction, fixedSize=(30, 30), 
			eventFilter=self)
		self.yesNoLayout = self.ui.createHLayout([self.ui.STRETCH, self.close, *between, self.ok, self.ui.STRETCH])
		self.mainLayout.addLayout(self.yesNoLayout)

	def eventFilter(self, object, event):
		return self.ui.buttonHoverEvent(objects=[
			[self.close, assetsPath.deleteHover, assetsPath.delete],
			[self.ok, assetsPath.successHover if not self.isError else assetsPath.success, assetsPath.success],
		], hoveredObject=object, event=event)

	def init(self):
		pass

	def openOtherModal(self, modalToggle):
		self.toggle()
		modalToggle()

	def willBeOpen(self, *args, **kwargs):
		pass

	def willBeClosed(self):
		pass