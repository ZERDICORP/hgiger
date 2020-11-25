from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QTabWidget, QComboBox, QLabel
from PyQt5.QtWidgets import QGridLayout, QFileDialog, QListWidgetItem, QLineEdit, QPushButton, QAbstractItemView, QListWidget
from PyQt5.QtGui import QPixmap, QIcon, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QSize, QEvent
from client.tools.staticManager import styles

def pomp(*args, **kwargs):
	pass

class UiTools(object):
	def byDefaultIcon(self, icon):
		return f"{self.manager.baseImagePath}/{icon}" if icon != self.defaultSectionIcon else icon

	def getFontHeight(self, fontSize):
		return QFontMetrics(QFont(self.RobotoLight)).size(fontSize, "A").height()

	def getFontWidth(self, fontSize, text):
		return QFontMetrics(QFont(self.RobotoLight)).size(fontSize, text).width()

	def createElidedText(self, font, text, width):
		return QFontMetrics(font).elidedText(text, Qt.ElideRight, width)

	def truncate(self, string, length):
		return string if len(string) < length + 1 else string[:length] + ".."

	def createHLayout(self, widgets, alignment=None):
		hbox = QHBoxLayout()
		if alignment:
			hbox.setAlignment(alignment)
		for i, widget in enumerate(widgets):
			if widget == self.STRETCH:
				hbox.addStretch(1)
			elif widget == self.STRETCHi:
				hbox.setStretch(1, i)
			elif type(widget) in [QHBoxLayout, QVBoxLayout, QGridLayout]:
				hbox.addLayout(widget, i)
			else:
				hbox.addWidget(widget, i)
		return hbox

	def createVLayout(self, widgets=[], alignment=None):
		vbox = QVBoxLayout()
		if alignment:
			vbox.setAlignment(alignment)
		for i, widget in enumerate(widgets):
			if widget == self.STRETCH:
				vbox.addStretch(1)
			elif widget == self.STRETCHi:
				vbox.setStretch(1, i)
			elif type(widget) in [QHBoxLayout, QVBoxLayout, QGridLayout]:
				vbox.addLayout(widget, i)
			else:
				vbox.addWidget(widget, i)
		return vbox

	def clearLayout(self, layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()

	def createLineEdit(self, text="", placeholder="", objectName=None, alignment=Qt.AlignLeft, fontSize=12, returnAction=pomp, inputAction=pomp):
		lineEdit = QLineEdit()
		lineEdit.setText(text)
		lineEdit.setObjectName(objectName)
		lineEdit.setPlaceholderText(placeholder)
		lineEdit.setAlignment(alignment)
		lineEdit.setFont(QFont(self.RobotoLight, fontSize))
		lineEdit.returnPressed.connect(returnAction)
		lineEdit.textChanged.connect(inputAction)
		return lineEdit

	def createPushButton(self, iconPath="", text="", objectName=None, fixedSize=None, fontSize=12, action=pomp, eventFilter=None):
		pushButton = QPushButton(QIcon(iconPath), text)
		pushButton.setObjectName("menuButton" if not objectName else objectName)
		if fixedSize:
			pushButton.setFixedSize(QSize(*fixedSize))
		pushButton.setFont(QFont(self.RobotoLight, fontSize))
		pushButton.setCursor(self.CursorPointer)
		pushButton.installEventFilter(eventFilter)
		pushButton.clicked.connect(action)
		return pushButton

	def createLabel(self, text="", alignment=Qt.AlignLeft, objectName=None, fontSize=12, tooltip=None):
		label = QLabel(text)
		label.setWordWrap(True)
		if tooltip:
			label.setToolTip(u'{}'.format(tooltip))
		label.setAlignment(alignment)
		label.setObjectName(objectName)
		label.setFont(QFont(self.RobotoLight, fontSize))
		return label

	def createZero(self, fontSize):
		zero = self.createLabel(text="ZERO", alignment=Qt.AlignCenter)
		zero.setStyleSheet(styles.zero)
		zero.setFont(QFont(self.RobotoBold, fontSize))
		return zero

	def createComboBox(self, items=[], fontSize=12, activated=pomp):
		comboBox = QComboBox()
		comboBox.addItems(items)
		comboBox.setFont(QFont(self.RobotoLight, fontSize))
		comboBox.setCursor(self.CursorPointer)
		comboBox.activated[int].connect(activated)
		return comboBox

	def createList(self):
		list = QListWidget()
		list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		list.verticalScrollBar().setSingleStep(12)
		return list

	def insertItemToList(self, list, item):
		itemWidget = QListWidgetItem(list)
		itemWidget.setSizeHint(item.sizeHint())
		list.addItem(itemWidget)
		list.setItemWidget(itemWidget, item)

	def createTabWidget(self, fontSize=12, objectName=None):
		tabWidget = QTabWidget()
		tabWidget.setObjectName(objectName)
		tabWidget.tabBar().setCursor(self.CursorPointer)
		tabWidget.tabBar().setFont(QFont(self.RobotoLight, fontSize))
		return tabWidget

	def createTextEdit(self, text="", placeholder="", objectName=None, readOnly=False, fontSize=12, inputAction=pomp):
		textEdit = QPlainTextEdit()
		textEdit.setPlaceholderText(placeholder)
		textEdit.setPlainText(text)
		textEdit.setObjectName(objectName)
		textEdit.textChanged.connect(inputAction)
		textEdit.setTabStopDistance(40)
		textEdit.setReadOnly(readOnly)
		textEdit.setFont(QFont(self.RobotoLight, fontSize))
		return textEdit

	def createPixmap(self, path=None, size=(40, 40), fontSize=12, objectName=None):
		pixmap = QLabel()
		pixmap.setObjectName(objectName)
		pixmap.setScaledContents(True)
		pixmap.setFont(QFont(self.RobotoLight, fontSize))
		if path:
			pixmap.setPixmap(QPixmap(path).scaled(*size, Qt.KeepAspectRatio))
		return pixmap

	def buttonHoverEvent(self, objects, hoveredObject, event):
		if event.type() == QEvent.Enter:
			for object, image, _ in objects:
				if object == hoveredObject:
					object.setIcon(QIcon(image))
			return True
		elif event.type() == QEvent.Leave:
			for object, _, image in objects:
				if object == hoveredObject:
					object.setIcon(QIcon(image))
			return True
		return False

	def openExplorer(self):
		options = QFileDialog.Options()
		fileName, _ = QFileDialog.getOpenFileName(self, "Open", "C:/Users/Kolya/", "All Files (*);;PNG files (*.png)", options=options)
		if fileName:
			return fileName