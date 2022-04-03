from core.workerTools import WorkerTools
from modules.genID import genID

class Worker(WorkerTools):		
	# (↓) [-CELL SECTIONS-]
	def addCellSection(self, currentSectionId, sectionName, sectionIcon):
		self.cellSections.insert(currentSectionId + 1, {
			"name": sectionName,
			"icon": sectionIcon
		})
		return self.cellSections
	def deleteCellSection(self, sectionId):
		self.deleteSectionIcon(self.cellSections[sectionId]["icon"])
		self.deleteImagesByCellSection(self.cellSections[sectionId]["name"])
		self.cells = [cell for cell in self.cells if cell["section"] != self.cellSections[sectionId]["name"]]
		del self.cellSections[sectionId]
		return self.cellSections, self.cells
	def renameCellSection(self, sectionId, newValue):
		for cell in self.cells:
			if cell["section"] == self.cellSections[sectionId]["name"]:
				cell["section"] = newValue
		self.cellSections[sectionId]["name"] = newValue
		return self.cellSections, self.cells
	def reiconCellSection(self, sectionId, newValue):
		self.deleteSectionIcon(self.cellSections[sectionId]["icon"])
		self.cellSections[sectionId]["icon"] = self.imageManager.saveImage(path=newValue)
		return self.cellSections
	def swapCellSections(self, sections):
		return [[section for section in self.cellSections if section["name"] == sectionName][0] for sectionName in sections]
	# (↓) [-CELLS-]
	def addCell(self, cellName, section):
		newCell = {
			"name": cellName,
			"section": section,
			"body": [
				[{
					"name": cellName, 
					"icon": "client/static/assets/section.png"
				}], 
				[]
			],
			"id": genID(150)
		}
		self.cells.insert(0, newCell)
		return self.cells
	def deleteCell(self, cellId):
		index = self.findElementById(elements=self.cells, id=cellId, onlyIndex=True)
		self.deleteImagesByCell(self.cells[index])
		del self.cells[index]
		return self.cells
	def renameCell(self, cellId, newValue):
		self.cells[self.findElementById(elements=self.cells, id=cellId, onlyIndex=True)]["name"] = newValue
		return self.cells
	def moveCell(self, cellId, newValue):	
		self.cells[self.findElementById(elements=self.cells, id=cellId, onlyIndex=True)]["section"] = newValue
		return self.cells
	# (↓) [-HINT SECTIONS-]
	def addHintSection(self, currentSectionId, sectionName, sectionIcon):
		self.cells[self.findElementById(elements=self.cells, id=self.currentCell["id"], onlyIndex=True)]["body"][0].insert(currentSectionId + 1, {
			"name": sectionName,
			"icon": sectionIcon
		})
		return self.cells
	def deleteHintSection(self, sectionId):
		index = self.findElementById(elements=self.cells, id=self.currentCell["id"], onlyIndex=True)
		self.deleteSectionIcon(self.hintSections[sectionId]["icon"])
		self.deleteImagesByHintSection(self.cells[index]["body"][0][sectionId]["name"])
		self.cells[index]["body"][1] = [hint for hint in self.cells[index]["body"][1] if hint["section"] != self.cells[index]["body"][0][sectionId]["name"]]
		del self.cells[index]["body"][0][sectionId]
		return self.cells
	def renameHintSection(self, sectionId, newValue):
		for hint in self.hints:
			if hint["section"] == self.hintSections[sectionId]["name"]:
				hint["section"] = newValue
		self.cells = self.updateHints(cells=self.cells, cellId=self.currentCell["id"], hints=self.hints)
		return self.updateHintSection(cells=self.cells, cellId=self.currentCell["id"],
			sectionId=sectionId, sectionName=newValue)
	def reiconHintSection(self, sectionId, newValue):
		self.deleteSectionIcon(self.hintSections[sectionId]["icon"])
		fileName = self.imageManager.saveImage(path=newValue)
		return self.updateHintSection(cells=self.cells, cellId=self.currentCell["id"],
			sectionId=sectionId, sectionIcon=fileName)
	def swapHintSections(self, sections):
		return self.updateHintSections(cells=self.cells, cellId=self.currentCell["id"], 
			sections=[[section for section in self.hintSections if section["name"] == sectionName][0] for sectionName in sections])
	# (↓) [-HINTS-]
	def addHint(self, hintName, section):
		newHint = {
			"name": hintName,
			"section": section,
			"id": genID(150),
			"images": [],
			"tags": ["example"],
			"pages": [{
				"content": "",
				"name": "page1"
			}]
		}
		self.cells[self.findElementById(elements=self.cells, id=self.currentCell["id"], onlyIndex=True)]["body"][1].insert(0, newHint)
		return self.cells
	def deleteHint(self, hintId):
		index = self.findElementById(elements=self.hints, id=hintId, onlyIndex=True)
		self.inThread(lambda: self.imageManager.deleteImages(self.hints[index]["images"]))
		del self.hints[index] 
		return self.updateHints(cells=self.cells, cellId=self.currentCell["id"], hints=self.hints)
	def renameHint(self, hintId, newValue):
		self.hints[self.findElementById(elements=self.hints, id=hintId, onlyIndex=True)]["name"] = newValue
		return self.updateHints(cells=self.cells, cellId=self.currentCell["id"], hints=self.hints)
	def moveHint(self, hintId, newPath):
		cellSection, cellId, hintSection = newPath
		hintIndex = self.findElementById(elements=self.hints, id=hintId, onlyIndex=True)
		cellIndex = self.findElementById(elements=self.cells, id=cellId, onlyIndex=True)
		self.hints[hintIndex]["section"] = hintSection
		self.cells = self.updateHints(cells=self.cells, cellId=self.currentCell["id"],
			hints=[hint for hint in self.hints if hint["id"] != hintId])
		self.cells[cellIndex]["body"][1].insert(0, self.hints[hintIndex])
		return self.cells
	# (↓) [-HINT-]
	def editTags(self, newTags):
		self.currentHint["tags"] = newTags
		return self.updateHint(cells=self.cells, cellId=self.currentCell["id"], hintId=self.currentHint["id"],
			hint=self.currentHint)
	def addPage(self, currentPageId, pageName):
		self.currentHint["pages"].insert(currentPageId + 1, {
			"name": pageName,
			"content": ""
		})
		return self.updateHint(cells=self.cells, cellId=self.currentCell["id"], hintId=self.currentHint["id"],
			hint=self.currentHint)
	def deletePage(self, pageId):
		del self.currentHint["pages"][pageId]
		return self.updateHint(cells=self.cells, cellId=self.currentCell["id"], hintId=self.currentHint["id"],
			hint=self.currentHint)
	def renamePage(self, pageId, newValue):
		self.currentHint["pages"][pageId]["name"] = newValue
		return self.updateHint(cells=self.cells, cellId=self.currentCell["id"], hintId=self.currentHint["id"],
			hint=self.currentHint)
	def swapPages(self, pages):
		self.currentHint["pages"] = [[page for page in self.currentHint["pages"] if page["name"] == pageName][0] for pageName in pages]
		return self.updateHint(cells=self.cells, cellId=self.currentCell["id"], hintId=self.currentHint["id"],
			hint=self.currentHint)
	def editPageText(self, pageId, newValue):
		self.currentHint["pages"][pageId]["content"] = newValue
		return self.updateHint(cells=self.cells, cellId=self.currentCell["id"], hintId=self.currentHint["id"],
			hint=self.currentHint)
	def addImage(self, imagePath):
		imagePath = self.imageManager.saveImage(path=imagePath)
		self.currentHint["images"].insert(0, imagePath)
		return self.updateHint(cells=self.cells, cellId=self.currentCell["id"], hintId=self.currentHint["id"],
			hint=self.currentHint)
	def deleteImage(self, imageId):
		self.inThread(lambda: self.imageManager.deleteImage(
			fileName=self.imageManager.getFileName(self.currentHint["images"][imageId])))
		del self.currentHint["images"][imageId]
		return self.updateHint(cells=self.cells, cellId=self.currentCell["id"], hintId=self.currentHint["id"],
			hint=self.currentHint)