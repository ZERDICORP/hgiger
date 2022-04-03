class TagFinderTools():
	def getTags(self, globalScope=True):
		tags = []
		for hint in self.hints:
			if not globalScope and hint["section"] != self.tabWidget.currentName():
				continue
			for tag in hint["tags"]:
				if tag not in tags:
					tags.append(tag)
		return tags
		
	def findByTags(self, tags):
		if not self.inGlobalScope:
			hints = [hint for hint in self.hints if any(tag in hint["tags"] for tag in tags)]
			topSection = [0, None]
			for index, section in enumerate(self.sections):
				count = 0
				for hint in hints:
					if hint["section"] == section:
						count += 1
				if count > topSection[0]:
					topSection = [count, index]
			return self.sortByTags(tags, self.tabWidget.currentName())
		else:
			return self.sortByTags(tags, None)

	def sortByTags(self, tags, section):
		hints = [hint for hint in self.hints if hint["section"] == section] if section else [hint for hint in self.hints]
		for i in range(len(hints)):
			tagCount = sum([1 for tag in tags if tag in hints[i]["tags"]])
			for j in range(len(hints)):
				if tagCount > sum([1 for tag in tags if tag in hints[j]["tags"]]):
					hints[i], hints[j] = hints[j], hints[i]
		return [hint for hint in hints if any([tag in hint["tags"] for tag in tags])]