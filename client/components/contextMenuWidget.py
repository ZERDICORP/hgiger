from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QFont
from client.tools.staticManager import styles

class ContextMenuWidget(QMenu):
	def __init__(self, parent, font, actions):
		super(ContextMenuWidget, self).__init__(parent)
		
		self.setFont(QFont(font, 10))
		self.setStyleSheet(styles.contextMenu)

		for arr in actions:
			action, trigger, disabled = arr
			if trigger:
				action.triggered.connect(trigger)
			action.setDisabled(disabled)
			self.addAction(action)