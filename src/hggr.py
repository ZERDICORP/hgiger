from sys import argv, executable
import sys
from os import listdir, getcwd, path, mkdir
from json import load
from threading import Thread
from modules.strDiff import strDiff

choiceIndex = None
choiceIndexCommand = "--i="

class Logger:
	HINT = "HINT"
	REMINDER = "REMINDER"
	NO_RESULTS = "NO_RESULTS"
	BAD_INDEX = "BAD_INDEX"
	INDEX_SHOULD_BE_INTEGER = "INDEX_SHOULD_BE_INTEGER"
	FILE_ALREADY_EXISTS = "FILE_ALREADY_EXISTS"
	FILE_CREATED = "FILE_CREATED"
	FILE_OVERWRITED = "FILE_OVERWRITED"
	MAYBE_YOU_MEAN_TAGS = "MAYBE_YOU_MEAN_TAGS"
	LINE = "LINE"
	isLoading = False
	loadingCount = 0
	def log(type=None, req={}, noPrint=False):
		res = ""
		if type == Logger.HINT:
			res = f"[{req['index']}]. [{req['section']} > \"{req['name']}\"] {{pages={req['pages']}}}"
		elif type == Logger.REMINDER:
			res = "[info]:\n\thgiger <tag>\n\tor\n\thgiger <tag1> <tag2> ... <tagN>"
		elif type == Logger.NO_RESULTS:
			res = "[info]: no results :\\"
		elif type == Logger.BAD_INDEX:
			res = f"[error]: index should be 0 to {req['len']}"
		elif type == Logger.INDEX_SHOULD_BE_INTEGER:
			res = f"[error]: index should be an integer"
		elif type == Logger.FILE_ALREADY_EXISTS:
			res = f"[info]: file \"{req['fileName']}\" already exists :["
		elif type == Logger.FILE_CREATED:
			res = f"[info]: file \"{req['fileName']}\" successfully created :]"
		elif type == Logger.FILE_OVERWRITED:
			res = f"[info]: file \"{req['fileName']}\" successfully overwrited :]"
		elif type == Logger.MAYBE_YOU_MEAN_TAGS:
			res = "[mym]:\n\t" + ", ".join([f"\"{tag[1]}\" ({tag[0]}%)" for tag in req["tags"]])
		if not noPrint:
			print(res)
		return res
	def draw(type, length):
		if type == Logger.LINE:
			print("-" * length)
	def startLoading():
		Logger.isLoading = True
		Logger.loadingCount = 0
		print("loading: [", end="")
		while Logger.isLoading:
			if Logger.loadingCount % 10000 == 0:
				print(".", end="")
			Logger.loadingCount += 1
	def stopLoading():
		Logger.isLoading = False
		print(f"] |{Logger.loadingCount // 10000 + 1}|")

def getTags():
	tags = []
	for cell in cells:
		for hint in cell["body"][1]:
			for tag in hint["tags"]:
				if tag not in tags:
					tags.append(tag)
	return tags

def maybeYouMean(tags):
	newTags = []
	for enteredTag in tags:
		maxProcentDiff = 0
		closestTag = None
		for tag in getTags():
			procentDiff = strDiff(tag, enteredTag)
			if procentDiff > maxProcentDiff:
				maxProcentDiff = int(procentDiff)
				closestTag = tag
		if closestTag:
			newTags.append([maxProcentDiff, closestTag])
	if newTags:
		Logger.log(type=Logger.MAYBE_YOU_MEAN_TAGS, req={"tags": newTags})

def sortByTags(tags, nextStep):
	hints = []
	for cell in cells:
		for hint in cell["body"][1]:
			hints.append(hint)
	for i in range(len(hints)):
		tagCount = sum([1 for tag in tags if tag in hints[i]["tags"]])
		for j in range(len(hints)):
			if tagCount > sum([1 for tag in tags if tag in hints[j]["tags"]]):
				hints[i], hints[j] = hints[j], hints[i]
	nextStep([hint for hint in hints if any([tag in hint["tags"] for tag in tags])])

def showHints(hints):
	maxLength = 0
	strings = []
	for i, hint in enumerate(hints):
		string = Logger.log(type=Logger.HINT, req={
			"index": i,
			"pages": len(hint['pages']), 
			"section": hint['section'], 
			"name": hint['name']
		}, noPrint=True)
		if len(string) > maxLength:
			maxLength = len(string)
		strings.append(string)
	Logger.draw(type=Logger.LINE, length=maxLength)
	for string in strings:
		print(string)
	Logger.draw(type=Logger.LINE, length=maxLength)

def saveFile(name, content):
	with open(f"{getcwd()}/{name}", "w", encoding="utf-8") as f:
		f.write(content)

def createFilesByPages(pages):
	for page in pages:
		pathArr = page["name"].split("/")
		path = "./"

		for i, item in enumerate(pathArr):
			if i < len(pathArr) - 1:
				path += item + "/"
				try:
					mkdir(path)
				except:
					continue
			else:
				if item not in listdir(path):
					saveFile(page["name"], page["content"])
					Logger.log(type=Logger.FILE_CREATED, req={"fileName": page["name"]})
				else:
					Logger.log(type=Logger.FILE_ALREADY_EXISTS, req={"fileName": page["name"]})
					overwrite = input("Overwrite it? (y): ")
					if overwrite in ["y", "Y", "yes"]:
						saveFile(page["name"], page["content"])
						Logger.log(type=Logger.FILE_OVERWRITED, req={"fileName": page["name"]})

def askIndex(hints):
	print("index: ", end="")
	index = input("") if not choiceIndex else print(choiceIndex) or choiceIndex
	if index:
		if index.isdigit():
			index = int(index)
			if index >= 0 and index < len(hints):
				createFilesByPages(pages=hints[index]["pages"])
			else:
				Logger.log(type=Logger.BAD_INDEX, req={"len": len(hints) - 1})
				askIndex(hints)
		else:
			Logger.log(type=Logger.INDEX_SHOULD_BE_INTEGER)
			askIndex(hints)
	else:
		sys.exit()

def checkHints(hints):
	Logger.stopLoading()
	if hints:
		showHints(hints)
		askIndex(hints)
	else:
		Logger.log(type=Logger.NO_RESULTS)
		maybeYouMean(argv)

def getExecutablePath():
	if getattr(sys, "frozen", False):
		application_path = path.dirname(sys.executable)
	elif __file__:
		application_path = path.dirname(__file__)
	return application_path

if __name__ == "__main__":
	with open(path.join(getExecutablePath(), "db/db.json")) as f:
		cellSections, cells = load(f)
	try:
		del argv[0]
		for index, item in enumerate(argv):
			if choiceIndexCommand in item:
				choiceIndex = item.replace(choiceIndexCommand, "")
				del argv[index]
		if argv:
			Thread(target=lambda: sortByTags(tags=argv, nextStep=checkHints)).start()
			Logger.startLoading()
		else:
			Logger.log(type=Logger.REMINDER)
	except KeyboardInterrupt:
		sys.exit()