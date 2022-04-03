from PyQt5.QtCore import Qt, QSize
from client.tools.staticManager import assetsPath, styles
from client.modals.modalWidget import ModalWidget

class TelegramModalWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(TelegramModalWidget, self).__init__(parent, ui)
		
		self.setStyleSheet("".join([
			styles.menuButton,
			styles.telegramModal,
		]))

		self.loader = self.ui.createLoader()
		self.token = self.ui.manager.hgigerbot.token
		self.chatId = self.ui.manager.hgigerbot.chatId

		self.title = self.ui.createLabel(text="HGiger TeleBot", fontSize=20)
		self.close = self.ui.createPushButton(iconPath=assetsPath.delete, action=self.toggle, fixedSize=(30, 30), 
			eventFilter=self)
		self.token = self.ui.createLabel(text=f"token: {self.ui.truncate(self.token, 5) + self.token[-5:]}", fontSize=14)
		self.chatId = self.ui.createLabel(text=f"chatId: {self.chatId}", fontSize=14)
		self.cloning = self.ui.createPushButton(iconPath=assetsPath.cloning, fixedSize=(40, 40), objectName="cloning", eventFilter=self,
			action=lambda: self.ui.questionModal.toggle(
				question="Cloning current database to telegram bot \"HGiger\"?",
				action=self.cloningDatabase))
		self.cloning.setIconSize(QSize(25, 25))

		self.mainLayout.addLayout(self.ui.createVLayout([
			self.ui.createHLayout([
				self.title, 
				self.close
			]),
			self.ui.createVLayout([
				self.token,
				self.chatId
			]),
			self.ui.createHLayout([self.cloning], alignment=Qt.AlignRight)
		], alignment=Qt.AlignTop))

		self.setMinimumWidth((int)(self.ui.WProperties[0][0] / 100 * 50))

		self.parent.setChild(self, alignment=Qt.AlignCenter)

	def cloningDatabase(self):
		self.loader.toggle()

		self.bot = self.ui.manager.hgigerbot.Bot(dbPath=self.ui.manager.basePath, hintsCount=self.ui.manager.hintsCount());
		self.bot.finish.connect(self.cloningFinished);
		self.bot.error.connect(lambda message: self.cloningError(errorMessage = message));
		self.bot.start();

	def cloningError(self, errorMessage):
		self.loader.toggle()
		self.ui.infoModal.toggle(info=errorMessage)

	def cloningFinished(self):
		self.loader.toggle()
		self.ui.infoModal.toggle(info="Success cloning database :]")

	def eventFilter(self, object, event):
		return self.ui.buttonHoverEvent(objects=[
			[self.close, assetsPath.deleteHover, assetsPath.delete],
			[self.cloning, assetsPath.cloningHover, assetsPath.cloning],
		], hoveredObject=object, event=event)
