from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt
from client.tools.staticManager import styles

class SmokeWidget(QFrame):
	def __init__(self, parent, ui):
		super(SmokeWidget, self).__init__(parent)
		
		self.setObjectName("parent")
		self.setStyleSheet(styles.smokeWidget)
		self.hide()

		self.ui = ui

		self.vbox = self.ui.createVLayout()

		self.setLayout(self.vbox)

	def open(self):
		self.child.init()
		self.resize(self.ui.size())
		self.show()

	def close(self):
		self.hide()

	def setChild(self, child=None, alignment=Qt.AlignVCenter, hideOnClick=True):
		self.child = child
		self.alignment = alignment
		self.hideOnClick = hideOnClick
		self.child.setObjectName("child")
		self.vbox.insertWidget(*(1, self.child, 1, self.alignment) if self.alignment else (1, self.child))

	def mousePressEvent(self, event):
		if self.hideOnClick:
			eX, eY = event.pos().x(), event.pos().y()
			x, y, w, h = self.child.pos().x(), self.child.pos().y(), self.child.width(), self.child.height()
			if (eX > x and eX < x + w) and (eY > y and eY < y + h):
				return
			self.child.toggle()