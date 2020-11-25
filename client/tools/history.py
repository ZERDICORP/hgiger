from client.pages.cellsPage import CellsPage
from client.pages.hintsPage import HintsPage
from client.pages.hintPage import HintPage

class History(object):
	def __init__(self):
		super(History, self).__init__()
		
		self.__types = [CellsPage, HintsPage, HintPage]
		self.__template = {
			"tabIndex": 0,
			"scrollLevel": 0,
			"tagFinder": False,
			"tagLine": "",
			"globalScope": True,
			"tagScrollLevel": 0,
			"attachedImages": False
		}
		self.__history = {
			CellsPage: {
				"tabIndex": 0,
				"scrollLevel": 0
			},
			HintsPage: {
				"tabIndex": 0,
				"scrollLevel": 0,
				"tagFinder": False,
				"tagLine": "",
				"globalScope": True,
				"tagScrollLevel": 0
			},
			HintPage: {
				"tabIndex": 0,
				"attachedImages": False
			}
		}

	def clearLast(self, obj):
		index = self.__types.index(type(obj))
		if index != len(self.__types) - 1:
			objType = self.__types[index + 1]
			for key in self.__history[objType]:
				self.__history[objType][key] = self.__template[key]

	def getHistory(self, obj):
		return self.__history[type(obj)]

	def updateTabIndex(self, obj, index):
		self.__history[type(obj)]["tabIndex"] = index

	def updateScrollLevel(self, obj, value):
		self.__history[type(obj)]["scrollLevel"] = value

	def updateTagFinder(self, obj, value):
		self.__history[type(obj)]["tagFinder"] = value

	def updateTagLine(self, obj, tagLine):
		self.__history[type(obj)]["tagLine"] = tagLine

	def updateGlobalScope(self, obj, value):
		self.__history[type(obj)]["globalScope"] = value

	def updateTagScrollLevel(self, obj, value):
		self.__history[type(obj)]["tagScrollLevel"] = value

	def updateAttachedImages(self, obj, value):
		self.__history[type(obj)]["attachedImages"] = value