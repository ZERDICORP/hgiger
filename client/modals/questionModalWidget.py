from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.modals.modalWidget import ModalWidget

class QuestionModalWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(QuestionModalWidget, self).__init__(parent, ui)
		
		self.setStyleSheet("".join([
			styles.menuButton
		]))
		
		self.question = self.ui.createLabel(alignment=Qt.AlignCenter, objectName="question", fontSize=18)

		self.mainLayout.addWidget(self.question)
		self.setYesNoButtons(yesAction=self.readyToAction)

		self.parent.setChild(self)

	def readyToAction(self):
		self.action()
		self.toggle()

	def willBeOpen(self, question, action):
		self.question.setText(question)
		self.action = action