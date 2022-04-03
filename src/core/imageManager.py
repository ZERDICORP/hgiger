import string, random, os
from shutil import copyfile
from threading import Thread

class ImageManager(object):
	def __init__(self, basePath):
		super(ImageManager, self).__init__()		
		self.basePath = basePath
	
	def getFileName(self, path):
		return path.split("/")[-1] if "/" in path else path.split("\\")[-1]

	def getName(self, fileName):
		return fileName.split(".")[0]

	def getFormat(self, fileName):
		return fileName.split(".")[1]

	def withoutSeparator(self, fileName):
		return f"{self.getName(fileName).split('____')[0]}.{self.getFormat(fileName)}"

	def createFileName(self, name, format):
		savedImagesList = os.listdir(self.basePath)
		newName = f"{name}____{''.join(random.choice(string.ascii_letters + string.digits) for i in range(15))}.{format}"
		if newName in savedImagesList:
			self.createFileName()
		return newName

	def saveImage(self, path):
		fileName = self.getFileName(path)
		fileName = self.createFileName(self.getName(fileName), self.getFormat(fileName))
		copyfile(path, f"{self.basePath}/{fileName}")
		return fileName

	def deleteImage(self, fileName):
		os.remove(f"{self.basePath}/{fileName}")

	def deleteImages(self, arr):
		for fileName in arr:
			self.deleteImage(fileName)