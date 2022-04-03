from PyQt5.QtWidgets import QToolTip
from PyQt5.QtGui import QCursor, QFont, QFontDatabase
from PyQt5.QtCore import Qt
from client.tools.staticManager import fontsPath
import subprocess

def GetSystemMetrics():
	p1 = subprocess.Popen(["xrandr"], stdout = subprocess.PIPE);
	p2 = subprocess.Popen(["grep", "*"], stdin = p1.stdout, stdout = subprocess.PIPE);
	p1.stdout.close();
	resolution = p2.communicate()[0].split()[0].decode("utf-8").split("x");
	return int(resolution[0]), int(resolution[1]);

class UiConst(object):
	def __init__(self):
		self.STRETCH = "STRETCH"
		self.STRETCHi = "STRETCHi"
		self.defaultSectionIcon = "client/static/assets/section.png"
		self.CursorPointer = QCursor(Qt.PointingHandCursor)
		self.CursorEdit = QCursor(Qt.IBeamCursor)
		self.sWH = GetSystemMetrics()
		self.RobotoLight = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(fontsPath.RobotoLight))[0]
		self.RobotoBold = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(fontsPath.RobotoBold))[0]
		QToolTip.setFont(QFont(self.RobotoLight, 10))