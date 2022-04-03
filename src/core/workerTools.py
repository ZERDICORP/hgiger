from threading import Thread

class WorkerTools(object):
	def __init__(self, baseImagePath, imageManager):
		super(WorkerTools, self).__init__()
		self.baseImagePath = baseImagePath
		self.imageManager = imageManager

	def update(self, manager):
		self.cellSections = manager.cellSections
		self.cells = manager.cells
		self.currentCell = manager.currentCell
		self.hintSections = manager.hintSections
		self.hints = manager.hints
		self.currentHint = manager.currentHint
		self.defaultSectionIcon = manager.builder.defaultSectionIcon

	def inThread(self, function):
		Thread(target=function).start()

	def deleteSectionsIcons(self, arr):
		for icon in arr:
			self.deleteSectionIcon(icon)

	def deleteSectionIcon(self, icon):
		if icon != self.defaultSectionIcon:
			self.inThread(lambda: self.imageManager.deleteImage(
				fileName=self.imageManager.getFileName(icon)))

	def deleteImagesByCellSection(self, cellSectionName):
		images = []
		cells = [cell for cell in self.cells if cell["section"] == cellSectionName]
		for cell in cells:
			for hint in cell["body"][1]:
				images += hint["images"]
			self.inThread(lambda: self.deleteSectionsIcons(
				[section["icon"] for section in cell["body"][0]]))
		self.inThread(lambda: self.imageManager.deleteImages(images))

	def deleteImagesByCell(self, cell):
		images = []
		for hint in cell["body"][1]:
			images += hint["images"]
		self.inThread(lambda: self.imageManager.deleteImages(images))
		self.inThread(lambda: self.deleteSectionsIcons(
			[section["icon"] for section in cell["body"][0]]))

	def deleteImagesByHintSection(self, hintSectionName):
		images = []
		hints = [hint for hint in self.hints if hint["section"] == hintSectionName]
		for hint in hints:
			images += hint["images"]
		self.inThread(lambda: self.imageManager.deleteImages(images))

	def findElementById(self, elements=None, id=None, onlyIndex=False):
		for index, element in enumerate(elements):
			if element["id"] == id:
				return index if onlyIndex else element

	def updateHintSections(self, cells, cellId, sections):
		cells[self.findElementById(elements=cells, id=cellId, onlyIndex=True)]["body"][0] = sections
		return cells

	def updateHintSection(self, cells=None, cellId=None, sectionId=None, sectionName=None, sectionIcon=None):
		index = self.findElementById(elements=cells, id=cellId, onlyIndex=True)
		if sectionName:
			cells[index]["body"][0][sectionId]["name"] = sectionName
		if sectionIcon:
			cells[index]["body"][0][sectionId]["icon"] = sectionIcon
		return cells

	def updateHints(self, cells, cellId, hints):
		cells[self.findElementById(elements=cells, id=cellId, onlyIndex=True)]["body"][1] = hints
		return cells

	def updateHint(self, cells, cellId, hintId, hint):
		index = self.findElementById(elements=cells, id=cellId, onlyIndex=True)
		cells[index]["body"][1][self.findElementById(elements=cells[index]["body"][1], id=hintId, onlyIndex=True)] = hint
		return cells