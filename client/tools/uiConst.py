from win32api import GetSystemMetrics
from PyQt5.QtWidgets import QToolTip
from PyQt5.QtGui import QCursor, QFont, QFontDatabase
from PyQt5.QtCore import Qt
from client.tools.staticManager import fontsPath

class UiConst(object):
	def __init__(self):
		self.STRETCH = "STRETCH"
		self.STRETCHi = "STRETCHi"
		self.defaultSectionIcon = "client/static/assets/section.png"
		self.CursorPointer = QCursor(Qt.PointingHandCursor)
		self.CursorEdit = QCursor(Qt.IBeamCursor)
		self.sWH = GetSystemMetrics(0), GetSystemMetrics(1)
		self.RobotoLight = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(fontsPath.RobotoLight))[0]
		self.RobotoBold = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(fontsPath.RobotoBold))[0]
		QToolTip.setFont(QFont(self.RobotoLight, 10))