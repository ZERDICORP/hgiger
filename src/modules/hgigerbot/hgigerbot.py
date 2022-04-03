import json, requests
import telegram
from datetime import datetime
from PyQt5 import QtCore

with open("modules/hgigerbot/config.json") as f:
	config = json.load(f)

token = config["token"]
chatId = config["chatId"]

class Bot(QtCore.QThread):
	finish = QtCore.pyqtSignal()
	error = QtCore.pyqtSignal(str)

	def __init__(self, dbPath, hintsCount):
		super(Bot, self).__init__()
		self.dbPath = dbPath;
		self.hintsCount = hintsCount;

	def run(self):
		try:
			tb = telegram.Bot(token=token);
			tb.send_document(chatId, open(self.dbPath, "rb"), caption=f"Database Cloning Log:\n* Date: [{datetime.now().strftime('%d.%m.%Y | %H:%M')}]\n* Hints: [{self.hintsCount}]");
			self.finish.emit();
		except requests.exceptions.ConnectionError:
			self.error.emit("Connection is very weak, repeat later..");
		except Exception as e:
			print("Error when trying to clone: " + str(e));
			self.error.emit("An error has occurred :[");
