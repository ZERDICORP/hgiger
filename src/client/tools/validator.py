import os.path
from client.tools.validateType import ValidateType

class Validator(object):
	def __init__(self):
		super(Validator, self).__init__()
		self.validateType = ValidateType()
	
	def validate(self, type, **validateData):
		response = ""
		if type == self.validateType.TEXT:
			response = self.byText(**validateData)
		elif type == self.validateType.SECTION_NAME:
			response = self.bySectionName(**validateData)
		elif type == self.validateType.ELEMENT_NAME:
			response = self.byElementName(**validateData)
		elif type == self.validateType.IMAGE_PATH:
			response = self.byImagePath(**validateData)
		elif type == self.validateType.ARR:
			response = self.byArr(**validateData)
		return response

	def byText(self, value, source):
		error = ""
		if len(value) == 0:
			error = "value length can not be a zero"
		return error

	def bySectionName(self, value="", source=None, sections=[]):
		error = ""
		if len(value) < 3:
			error = "value length should be > 2"
		elif value == source:
			error = "value has not changed"
		elif value in sections:
			error = "this name already exists"
		return error

	def byElementName(self, value="", source=None):
		error = ""
		if len(value) == 0:
			error = "value length can not be a zero"
		elif value == source:
			error = "value has not changed"
		return error

	def byImagePath(self, value="", source=None):
		error = ""
		if len(value) > 0:
			if not os.path.isfile(value) or value.split(".")[-1] not in ["png", "jpg", "ico"]:
				error = "this not an image file"
			elif value == source:
				error = "value has not changed"
		else:
			error = "path length can not be a zero"
		return error

	def byArr(self, value=[], source=None):
		error = ""
		if value == source:
			error = "value has not changed"
		return error