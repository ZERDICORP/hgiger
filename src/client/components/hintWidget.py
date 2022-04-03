from PyQt5.QtWidgets import QWidget, QAction
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from client.tools.staticManager import assetsPath, styles
from client.components.contextMenuWidget import ContextMenuWidget

class HintWidget(QWidget):
	def __init__ (self, ui, hint, findedTags, parentWidth):
		super(HintWidget, self).__init__(None)

		self.installEventFilter(self)
		self.setStyleSheet(styles.listItem)

		self.ui = ui
		self.hint = hint
		self.findedTags = findedTags
		self.parentWidth = parentWidth

		self.vbox = self.ui.createVLayout()

		self.icon = self.ui.createLabel()
		self.icon.setScaledContents(True)
		self.icon.setPixmap(QPixmap(assetsPath.hint).scaled(30, 35))
		self.icon.setFixedSize(30, 35)

		self.name = self.ui.createLabel(objectName="name", tooltip=self.hint["name"], 
			fontSize=14, alignment=Qt.AlignVCenter)
		self.name.setText(self.ui.createElidedText(font=self.name.font(), 
			text=self.hint["name"], width=self.parentWidth))
		self.name.setMinimumHeight(40)
		self.name.setMaximumHeight(40)

		self.vbox.addLayout(self.ui.createHLayout([
			self.icon, 
			self.name
		]), 0)

		if self.hint["tags"] and self.findedTags:
			coincidence = [f"#{tag}" for tag in self.hint["tags"] if tag in self.findedTags]
			if coincidence:
				self.tags = self.ui.createLabel(objectName="tags", tooltip="   ".join(coincidence), fontSize=10)
				self.tags.setText(self.ui.createElidedText(font=self.tags.font(), 
					text="   ".join(coincidence), width=self.parentWidth))
				self.vbox.addWidget(self.tags, 1)

		self.setLayout(self.vbox)
		self.setCursor(self.ui.CursorPointer)

	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.ui.openPage(pageCreator=lambda: self.ui.createHintPage(self.hint["id"]))

	def contextMenuEvent(self, event):
		contextMenu = ContextMenuWidget(self, self.ui.RobotoLight, [
			[QAction(QIcon(assetsPath.rename), "Rename", self), lambda: self.ui.inputModal.toggle(
				validateData={"type": self.ui.validator.validateType.ELEMENT_NAME},
				value=self.hint["name"],
				action=lambda text: self.ui.manager.reception(self.ui.manager.requestType.RENAME_HINT,
					hintId=self.hint["id"],
					newValue=text)),
			False],
			[QAction(QIcon(assetsPath.move), "Move", self), lambda: self.ui.moveHintModal.toggle(
				objectName=self.hint["name"],
				objectId=self.hint["id"],
				objectSection=self.hint["section"]), 
			self.ui.moveHintModal.haveAnyReasonToOpen(objectSection=self.hint["section"])],
			[QAction(QIcon(assetsPath.delete), "Delete", self), lambda: self.ui.questionModal.toggle(
				question=f'Delete hint "{self.ui.truncate(string=self.hint["name"], length=30)}"?', 
				action=lambda: self.ui.manager.reception(self.ui.manager.requestType.DELETE_HINT,
					hintId=self.hint["id"])), 
			False]
		])
		contextMenu.exec_(self.mapToGlobal(event.pos()))