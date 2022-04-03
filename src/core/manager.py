import json
from threading import Thread
from modules.hgigerbot import hgigerbot
from core.imageManager import ImageManager
from core.worker import Worker
from core.requestType import RequestType

class Manager(object):
	def __init__(self):
		super(Manager, self).__init__()
		self.basePath = "db/db.json"
		self.baseImagePath = "db/images"
		self.hgigerbot = hgigerbot
		self.imageManager = ImageManager(basePath=self.baseImagePath)
		self.worker = Worker(self.baseImagePath, self.imageManager)
		self.requestType = RequestType()
		self.currentCell = {}
		self.hints = []
		self.hintSections = []
		self.currentHint = {}

	def inThread(self, function):
		Thread(target=function).start()

	def hintsCount(self):
		return sum([len(cell["body"][1]) for cell in self.cells])

	def setBuilder(self, builder):
		self.builder = builder

	def openCell(self, cellId):
		self.currentCell = self.worker.findElementById(elements=self.cells, id=cellId)
		self.hintSections, self.hints = self.currentCell["body"][0], self.currentCell["body"][1]

	def openHint(self, hintId):
		self.currentHint = [hint for hint in self.hints if hint["id"] == hintId][0]

	def save(self):
		with open(self.basePath, "w") as f:
			json.dump([self.cellSections, self.cells], f, sort_keys=True, indent=4)

	def load(self):
		with open(self.basePath) as f:
			self.cellSections, self.cells = json.load(f)

	def reception(self, type, **request):
		self.worker.update(self)
		# (↓) [-CELL SECTIONS-]
		if type == self.requestType.ADD_CELL_SECTION:
			self.cellSections = self.worker.addCellSection(**request)
		elif type == self.requestType.DELETE_CELL_SECTION:
			self.cellSections, self.cells = self.worker.deleteCellSection(**request)
		elif type == self.requestType.RENAME_CELL_SECTION:
			self.cellSections, self.cells = self.worker.renameCellSection(**request)
		elif type == self.requestType.REICON_CELL_SECTION:
			self.cellSections = self.worker.reiconCellSection(**request)
		elif type == self.requestType.SWAP_CELL_SECTIONS:
			self.cellSections = self.worker.swapCellSections(**request)
		# (↓) [-CELL-]
		elif type == self.requestType.ADD_CELL:
			self.cells = self.worker.addCell(**request)
		elif type == self.requestType.DELETE_CELL:
			self.cells = self.worker.deleteCell(**request)
		elif type == self.requestType.RENAME_CELL:
			self.cells = self.worker.renameCell(**request)
		elif type == self.requestType.MOVE_CELL:
			self.cells = self.worker.moveCell(**request)
		# (↓) [-HINT SECTIONS-]
		elif type == self.requestType.ADD_HINT_SECTION:
			self.cells = self.worker.addHintSection(**request)
		elif type == self.requestType.DELETE_HINT_SECTION:
			self.cells = self.worker.deleteHintSection(**request)
		elif type == self.requestType.RENAME_HINT_SECTION:
			self.cells = self.worker.renameHintSection(**request)
		elif type == self.requestType.REICON_HINT_SECTION:
			self.cells = self.worker.reiconHintSection(**request)
		elif type == self.requestType.SWAP_HINT_SECTIONS:
			self.cells = self.worker.swapHintSections(**request)
		# (↓) [-HINTS-]
		elif type == self.requestType.ADD_HINT:
			self.cells = self.worker.addHint(**request)
		elif type == self.requestType.DELETE_HINT:
			self.cells = self.worker.deleteHint(**request)
		elif type == self.requestType.RENAME_HINT:
			self.cells = self.worker.renameHint(**request)
		elif type == self.requestType.MOVE_HINT:
			self.cells = self.worker.moveHint(**request)
		# (↓) [-HINT-]
		elif type == self.requestType.EDIT_TAGS:
			self.cells = self.worker.editTags(**request)
		elif type == self.requestType.ADD_PAGE:
			self.cells = self.worker.addPage(**request)
		elif type == self.requestType.DELETE_PAGE:
			self.cells = self.worker.deletePage(**request)
		elif type == self.requestType.RENAME_PAGE:
			self.cells = self.worker.renamePage(**request)
		elif type == self.requestType.SWAP_PAGES:
			self.cells = self.worker.swapPages(**request)
		elif type == self.requestType.EDIT_PAGE_TEXT:
			self.cells = self.worker.editPageText(**request)
		elif type == self.requestType.ADD_IMAGE:
			self.cells = self.worker.addImage(**request)
		elif type == self.requestType.DELETE_IMAGE:
			self.cells = self.worker.deleteImage(**request)

		self.inThread(function=self.save)
		self.builder.rebuild()