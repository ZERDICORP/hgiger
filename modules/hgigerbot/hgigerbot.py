import json, requests
from telebot import TeleBot
from datetime import datetime

with open("modules/hgigerbot/config.json") as f:
	config = json.load(f)

token = config["token"]
chatId = config["chatId"]

def cloningDatabase(dbPath, hintsCount, cloningFinished, cloningError):
	try:
		TeleBot(token).send_document(chatId, open(dbPath, "rb"), 
			caption=f"Database Cloning Log:\n* Date: [{datetime.now().strftime('%d.%m.%Y | %H:%M')}]\n* Hints: [{hintsCount}]")
		cloningFinished()
	except requests.exceptions.ConnectionError:
		cloningError(errorMessage="Connection is very weak, repeat later..")
	except:
		cloningError(errorMessage="An error has occurred :[")