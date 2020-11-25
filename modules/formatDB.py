import json
from genID import genID

basePath = "../db/db.json"

sections, cells = json.load(open(basePath, "r"))

def save(sections, cells):
	with open(basePath, "w") as f:
		json.dump([sections, cells], f, sort_keys=True, indent=4)

def formatSections(sections):
	for i, section in enumerate(sections):
		newSection = {
			"name": section,
			"icon": "client/static/assets/section.png"
		}

		sections[i] = newSection

	return sections

def formatCells(cells):
	for i, cell in enumerate(cells):
		newCell = {
			"body": [formatSections(cell["cell"][0]), cell["cell"][1]],
			"id": genID(150),
			"name": cell["name"],
			"section": cell["db"]
		}
		cells[i] = newCell

	save(sections, cells)

def formatHints(cells):
	for i, cell in enumerate(cells):
		for j, hint in enumerate(cell["body"][1]):
			newHint = {
				"id": genID(150),
				"images": [image.split("/")[-1] for image in hint["imgs"]],
				"name": hint["name"],
				"section": hint["giger"],
				"tags": hint["tags"],
				"pages": [{"name": key, "content": hint["hint"][key]} for key in hint["hint"]]
			}

			cells[i]["body"][1][j] = newHint

	save(sections, cells)

def top(cells):
	hints = []
	for i, cell in enumerate(cells):
		for j, hint in enumerate(cell["body"][1]):
			hints.append([hint, [i, j]])

	for i in range(len(hints)):
		for j in range(len(hints)):
			if len(hints[i][0]["tags"]) > len(hints[j][0]["tags"]):
				hints[i], hints[j] = hints[j], hints[i]

	print(cells[hints[3][1][0]]["body"][1][hints[3][1][1]]["tags"])

save(formatSections(sections), cells)
formatCells(cells)
formatHints(cells)