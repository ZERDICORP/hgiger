from PyQt5.QtWidgets import QMainWindow, QWidget, QShortcut
from PyQt5.QtGui import QIcon, QFont, QKeySequence
from client.tools.uiConst import UiConst
from client.tools.uiTools import UiTools 
from client.tools.validator import Validator
from client.tools.staticManager import assetsPath, styles
from client.components.mainWindowWidget import MainWindow
from client.components.smokeWidget import SmokeWidget
from client.modals.cloneMenuModalWidget import CloneMenuModalWidget
from client.modals.getImagePathModalWidget import GetImagePathModalWidget
from client.modals.questionModalWidget import QuestionModalWidget
from client.modals.infoModalWidget import InfoModalWidget
from client.modals.moveCellModalWidget import MoveCellModalWidget
from client.modals.addSectionModalWidget import AddSectionModalWidget
from client.modals.addElementModalWidget import AddElementModalWidget
from client.modals.moveHintModalWidget import MoveHintModalWidget
from client.modals.inputModalWidget import InputModalWidget
from client.modals.tagsModalWidget import TagsModalWidget
from client.modals.textModalWidget import TextModalWidget
from client.modals.swapSectionsModalWidget import SwapSectionsModalWidget
from client.modals.loaderWidget import LoaderWidget
from client.modals.telegramModalWidget import TelegramModalWidget

class UI(MainWindow, UiConst, UiTools):
	def __init__(self):
		super(UI, self).__init__()
		
		self.setWindowIcon(QIcon(assetsPath.ico))
		self.setWindowTitle(" ")
		self.setStyleSheet(styles.window)	

		self.validator = Validator()
		self.WProperties = [
			[*self.WSize], 
			lambda: [
				self.mapToGlobal(self.pos()).x(), 
				self.mapToGlobal(self.pos()).y()
			]
		]

	def createLoader(self):
		return LoaderWidget(parent=self.createSmokeWidget(), ui=self)

	def createSmokeWidget(self):
		return SmokeWidget(self.centralWidget(), self)

	def setModals(self):
		self.telegramModal = TelegramModalWidget(parent=self.createSmokeWidget(), ui=self)
		self.cloneMenuModal = CloneMenuModalWidget(parent=self.createSmokeWidget(), ui=self)
		QShortcut(QKeySequence("Ctrl+M"), self.centralWidget()).activated.connect(self.cloneMenuModal.toggle)
		# (↓) [-TOP LEVEL-]
		self.getImagePathModal = GetImagePathModalWidget(parent=self.createSmokeWidget(), ui=self)
		self.questionModal = QuestionModalWidget(parent=self.createSmokeWidget(), ui=self)		
		self.addSectionModal = AddSectionModalWidget(parent=self.createSmokeWidget(), ui=self)
		self.addElementModal = AddElementModalWidget(parent=self.createSmokeWidget(), ui=self)
		self.moveCellModal = MoveCellModalWidget(parent=self.createSmokeWidget(), ui=self)
		self.moveHintModal = MoveHintModalWidget(parent=self.createSmokeWidget(), ui=self)
		self.inputModal = InputModalWidget(parent=self.createSmokeWidget(), ui=self)
		self.tagsModal = TagsModalWidget(parent=self.createSmokeWidget(), ui=self)
		self.textModal = TextModalWidget(parent=self.createSmokeWidget(), ui=self)
		self.swapSectionsModal = SwapSectionsModalWidget(parent=self.createSmokeWidget(), ui=self)
		self.infoModal = InfoModalWidget(parent=self.createSmokeWidget(), ui=self)