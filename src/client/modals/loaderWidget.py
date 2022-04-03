from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QSize
from client.tools.staticManager import gifsPath, styles
from client.modals.modalWidget import ModalWidget

class LoaderWidget(ModalWidget):
	def __init__(self, parent, ui):
		super(LoaderWidget, self).__init__(parent, ui)

		self.setStyleSheet("".join([
			styles.menuButton,
			styles.loader
		]))
		
		self.parent.setStyleSheet(styles.loader)

		self.loader = QMovie(gifsPath.loading)
		
		self.loadWrapper = self.ui.createLabel()
		self.loadWrapper.setMovie(self.loader)
		self.loadWrapper.movie().setScaledSize(QSize(100, 100))

		self.loader.start()

		self.mainLayout.addLayout(self.ui.createHLayout([
			self.loadWrapper
		], alignment=Qt.AlignCenter))

		self.parent.setChild(self, hideOnClick=False)